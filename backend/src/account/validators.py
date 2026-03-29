import re
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from django.utils import timezone


# Валидатор пароля на минимальную длину
class CustomMinimumLengthValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _(f'Пароль слишком короткий. Минимум {self.min_length} символов.'),
                code='password_too_short',
            )


# Валидатор для телефона, который проверяет, что телефон начинается с '+79'
phone_regex = RegexValidator(
    regex=r'^\+7\s\d{3}\s\d{3}\s\d{2}\s\d{2}$',
    message='Номер телефона должен быть в формате: +7 999 999 99 99.'
)


# Валидатор для проверки даты рождения
def validate_not_future(value):
    if value > timezone.localdate():
        raise ValidationError('Дата рождения не может быть в будущем.')
    