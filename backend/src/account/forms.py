from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.forms import SetPasswordForm

# Форма входа в систему
# Используется для аутентификации пользователей по email
class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email',
            'autocomplete': 'email',
        })
    )
    
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'autocomplete': 'current-password',
        })
    )


# Модель пользователя
User = get_user_model()


# Форма для изменения email при регистрации (до активации)
class RegistrationEmailChangeForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Новый email',
            'autocomplete': 'email',
        })
    )

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').lower()
        qs = User.objects.filter(email__iexact=email)
        if self.user:
            qs = qs.exclude(pk=self.user.pk)
        if qs.exists():
            raise ValidationError('Пользователь с таким email уже зарегистрирован')
        return email


# Форма регистрации наследуется от UserCreationForm:
# Содержит поля password1/password2, проверку совпадения и валидаторы пароля.
# Автоматически хеширует пароль (set_password).
# Подставляем наш CustomUser (email как логин) и ставим is_active=False до активации.
class RegistrationForm(UserCreationForm):
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Фамилия',
        })
    )

    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя',
        })
    )

    middle_name = forms.CharField(
        label='Отчество',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Отчество',
        })
    )
    
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            'autocomplete': 'email'
        })
    )

    # Поля пароля (наследуются от UserCreationForm)
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'autocomplete': 'new-password',
        })
    )

    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
            'autocomplete': 'new-password',
        })
    )

    # Метаданные формы
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('last_name', 'first_name', 'middle_name', 'email',)

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже зарегистрирован')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()

        return user


# Форма для изменения пароля, наследуется от PasswordChangeForm - стандартной формы Django для изменения пароля
# Используется для изменения пароля пользователя
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Старый пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Старый пароль',
            'autocomplete': 'current-password',
        })
    )

    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Новый пароль',
            'autocomplete': 'new-password',
        })
    )

    new_password2 = forms.CharField(
        label='Подтвердите новый пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите новый пароль',
            'autocomplete': 'new-password',
        })
    )


# Форма для сброса пароля
class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email',
            'autocomplete': 'on',
        })
    )


# Форма для повторной отправки письма с активацией
class ResendActivationForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email',
            'autocomplete': 'on',
        })
    )


# Форма для смены пароля
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Новый пароль',
            'autocomplete': 'on',
        })
    )
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
            'autocomplete': 'on',
        })
    )
