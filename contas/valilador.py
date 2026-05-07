import re
from django.core.exceptions import ValidationError


def valida_cpf(value):
    cpf = re.sub(r'\D', '', value)

    if len(cpf) != 11:
        raise ValidationError('CPF deve ter 11 dígitos')

    if cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido')

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    dig1 = (soma * 10 % 11) % 10

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    dig2 = (soma * 10 % 11) % 10

    if cpf[-2:] != f"{dig1}{dig2}":
        raise ValidationError('CPF inválido')