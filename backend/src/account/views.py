import logging
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.http import require_POST

from .forms import (
    CustomPasswordChangeForm,
    CustomSetPasswordForm,
    LoginForm,
    PasswordResetRequestForm,
    RegistrationEmailChangeForm,
    RegistrationForm,
    ResendActivationForm,
)
from .tokens import account_activation_token, password_reset_token
from .utils_jwt import clear_jwt_cookies, set_jwt_cookies

logger = logging.getLogger(__name__)
User = get_user_model()

REGISTRATION_SESSION_TTL = timedelta(hours=24)
REGISTRATION_USER_ID_KEY = "registration_user_id"
REGISTRATION_CREATED_TS_KEY = "registration_created_ts"


def _mask_email(email):
    if not email or "@" not in email:
        return None
    local, domain = email.split("@", 1)
    if not local:
        return None
    if len(local) == 1:
        masked_local = f"{local}***"
    else:
        masked_local = f"{local[0]}***{local[-1]}"
    return f"{masked_local}@{domain}"


def _get_safe_redirect_url(request, next_url):
    default_redirect = getattr(settings, "LOGIN_REDIRECT_URL", "/")
    if next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return default_redirect


def _clear_registration_session(request):
    request.session.pop(REGISTRATION_USER_ID_KEY, None)
    request.session.pop(REGISTRATION_CREATED_TS_KEY, None)


def _get_registration_user(request):
    user_id = request.session.get(REGISTRATION_USER_ID_KEY)
    created_ts = request.session.get(REGISTRATION_CREATED_TS_KEY)
    if not user_id or not created_ts:
        return None

    try:
        created_ts = float(created_ts)
    except (TypeError, ValueError):
        _clear_registration_session(request)
        return None

    ttl_seconds = REGISTRATION_SESSION_TTL.total_seconds()
    if timezone.now().timestamp() - created_ts > ttl_seconds:
        _clear_registration_session(request)
        return None

    user = User.objects.filter(pk=user_id, is_active=False).first()
    if not user:
        _clear_registration_session(request)
        return None
    return user


def _issue_registration_session(request, user):
    request.session[REGISTRATION_USER_ID_KEY] = user.pk
    request.session[REGISTRATION_CREATED_TS_KEY] = timezone.now().timestamp()


def _send_activation_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    activation_url = request.build_absolute_uri(
        reverse("account:activate", kwargs={"uidb64": uid, "token": token})
    )

    subject = "Подтверждение email"
    message = render_to_string(
        "account/activation_email.html",
        {
            "user": user,
            "activation_url": activation_url,
            "uid": uid,
            "token": token,
        },
    )
    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = "html"
    try:
        email.send(fail_silently=False)
    except Exception:
        logger.exception("Failed to send activation email to %s", user.email)


def user_login(request):
    next_url = request.GET.get("next") or request.POST.get("next")
    redirect_url = _get_safe_redirect_url(request, next_url)

    if getattr(request, "user", None) and request.user.is_authenticated:
        return redirect(redirect_url)

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = (cd.get("email") or "").lower()
            user = authenticate(request, email=email, password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    response = redirect(redirect_url)
                    set_jwt_cookies(response, user)
                    messages.success(request, "Вы успешно вошли в систему.")
                    return response
                messages.error(request, "Аккаунт не активирован. Подтвердите email.")
            else:
                messages.error(request, "Неверный логин или пароль.")
        else:
            messages.error(request, "Исправьте ошибки в форме и попробуйте снова.")
    else:
        form = LoginForm()

    return render(request, "account/login.html", {"form": form, "next": next_url})


def user_logout(request):
    logout(request)
    response = redirect("account:login")
    clear_jwt_cookies(response)
    messages.success(request, "Вы вышли из системы.")
    return response


def registry(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            _issue_registration_session(request, user)
            _send_activation_email(user, request)
            return redirect("account:activation_sent")

        non_required_errors = []
        for field_name, errors in form.errors.as_data().items():
            for err in errors:
                if err.code == "required":
                    continue
                label = form.fields.get(field_name).label if field_name in form.fields else ""
                prefix = f"{label}: " if label else ""
                non_required_errors.append(f"{prefix}{err.message}")

        for err_msg in non_required_errors:
            messages.error(request, err_msg)

        if not non_required_errors:
            messages.error(request, "Исправьте ошибки в форме и попробуйте снова.")
    else:
        form = RegistrationForm()

    return render(request, "account/registry.html", {"form": form})


def activation_sent(request):
    user = _get_registration_user(request)
    context = {
        "masked_email": _mask_email(user.email) if user else None,
        "can_change_email": bool(user),
        "change_email_form": RegistrationEmailChangeForm(user=user) if user else RegistrationEmailChangeForm(),
    }
    return render(request, "account/activation_sent.html", context)


@require_POST
def activation_email_change(request):
    user = _get_registration_user(request)
    if not user:
        messages.error(request, "Сессия регистрации не найдена. Попробуйте зарегистрироваться заново.")
        return redirect("account:registry")

    form = RegistrationEmailChangeForm(request.POST, user=user)
    if not form.is_valid():
        for field_errors in form.errors.values():
            for err in field_errors:
                messages.error(request, err)
        return redirect("account:activation_sent")

    new_email = form.cleaned_data["email"].lower()
    if user.is_active:
        messages.info(request, "Аккаунт уже активирован. Войдите в систему.")
        return redirect("account:login")

    if new_email != user.email:
        user.email = new_email
        user.save(update_fields=["email"])

    _issue_registration_session(request, user)
    _send_activation_email(user, request)
    messages.success(request, "Письмо с активацией отправлено на новый email.")
    return redirect("account:activation_sent")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])
        _clear_registration_session(request)
        login(request, user)
        response = redirect("account:activation_end")
        set_jwt_cookies(response, user)
        return response

    return redirect("account:activation_invalid")


def activation_end(request):
    return render(request, "account/activation_end.html")


def activation_invalid(request):
    return render(request, "account/activation_invalid.html")


def activation_resend(request):
    if request.method == "POST":
        form = ResendActivationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].lower()
            user = User.objects.filter(email__iexact=email, is_active=False).first()
            if user:
                _send_activation_email(user, request)

            messages.info(request, "Если такой email зарегистрирован, мы отправили письмо.")
            return redirect("account:activation_resend")
    else:
        form = ResendActivationForm()

    return render(request, "account/activation_resend.html", {"form": form})


@login_required
def password_change(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            response = redirect("account:password_change_done")
            set_jwt_cookies(response, user)
            messages.success(request, "Пароль изменён.")
            return response
        messages.error(request, "Исправьте ошибки в форме и попробуйте снова.")
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, "account/password_change.html", {"form": form})


@login_required
def password_change_done(request):
    return render(request, "account/password_change_done.html")


def password_reset(request):
    if request.user.is_authenticated:
        messages.info(request, "Вы уже авторизованы, сменить пароль можно в личном кабинете.")
        return redirect("account:password_change")

    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].lower()
            user = User.objects.filter(email__iexact=email, is_active=True).first()
            if user:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = password_reset_token.make_token(user)
                reset_url = request.build_absolute_uri(
                    reverse("account:password_reset_confirm", kwargs={"uidb64": uid, "token": token})
                )

                subject = "Восстановление пароля"
                html = render_to_string(
                    "account/password_reset_email.html",
                    {"user": user, "reset_url": reset_url},
                )
                msg = EmailMessage(subject, html, to=[user.email])
                msg.content_subtype = "html"
                try:
                    msg.send(fail_silently=False)
                except Exception:
                    logger.exception("Failed to send password reset email to %s", user.email)

            return redirect("account:password_reset_end")
        messages.error(request, "Исправьте ошибки в форме и попробуйте снова.")
    else:
        form = PasswordResetRequestForm()

    return render(request, "account/password_reset_form.html", {"form": form})


def password_reset_end(request):
    return render(request, "account/password_reset_end.html")


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and password_reset_token.check_token(user, token):
        if request.method == "POST":
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                response = redirect("account:password_reset_complete")
                clear_jwt_cookies(response)
                messages.success(request, "Пароль обновлён. Войдите снова.")
                return response
        else:
            form = CustomSetPasswordForm(user)
        return render(request, "account/password_reset_confirm.html", {"form": form, "validlink": True})

    return render(request, "account/password_reset_confirm.html", {"validlink": False})


def password_reset_complete(request):
    return render(request, "account/password_reset_complete.html")
