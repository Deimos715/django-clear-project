from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Токен активации учётной записи
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # is_active участвует в хэше -> после активации токен перестанет подходить
        return f"{user.pk}{timestamp}{user.is_active}"

account_activation_token = AccountActivationTokenGenerator()

# Токен сброса пароля
class PasswordResetTokenGeneratorStrict(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Токен сброса: инвалидируется после смены пароля и (дополнительно) после входа
        last_login_part = ""
        if user.last_login:
            # Используем целочисленный Unix timestamp для однозначного представления времени
            # Это избегает проблем с часовыми поясами и микросекундами
            try:
                last_login_part = str(int(user.last_login.timestamp()))
            except Exception:
                # На случай неожиданных значений fallback на isoformat без микросекунд
                last_login_part = user.last_login.replace(microsecond=0).isoformat()
        return f"{user.pk}{user.password}{last_login_part}{timestamp}"

password_reset_token = PasswordResetTokenGeneratorStrict()