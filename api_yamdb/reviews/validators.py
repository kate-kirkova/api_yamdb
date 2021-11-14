from django.utils import timezone
from rest_framework.validators import ValidationError


def year_validator(value):
    ''' Кастомный валидатор для года выхода произведения '''
    if value < 1000:
        raise ValidationError('Мы не храним такое старье')
    if value > timezone.now().year:
        raise ValidationError(
            'Марти, ты вернулся из будущего?')
