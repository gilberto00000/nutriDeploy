from django.contrib.auth.models import AbstractUser
from django.db import models
from .valilador import valida_cpf


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('nutritionist', 'Nutricionista'),
        ('patient', 'Paciente'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.username
    
    
class Profile(models.Model):
    user = models.OneToOneField('contas.User', on_delete=models.CASCADE, related_name='profile')

    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True, validators=[valida_cpf])
    phone = models.CharField(max_length=20, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    crn = models.CharField(max_length=20, null=True, blank=True)
    specialty = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user}"
    