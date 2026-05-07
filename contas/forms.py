from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import transaction

from .models import User
from usuarios.models import Patient


class BaseSignupForm(UserCreationForm):
    username = forms.CharField(label='Nome de usuario', max_length=150)
    first_name = forms.CharField(label='Nome', max_length=150)
    email = forms.EmailField(label='E-mail', required=False)
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'email')


class NutritionistSignupForm(BaseSignupForm):
    crn = forms.CharField(max_length=20, label='CRN')
    specialty = forms.CharField(max_length=100, label='Especialidade')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'nutritionist'
        if commit:
            user.save()
            profile = user.profile
            profile.crn = self.cleaned_data['crn']
            profile.specialty = self.cleaned_data['specialty']
            profile.save()
        return user


class PatientSignupForm(BaseSignupForm):
    birth_date = forms.DateField(label='Data de nascimento', widget=forms.DateInput(attrs={'type': 'date'}))
    sex = forms.ChoiceField(label='Sexo', choices=Patient.SEX_CHOICES)
    height = forms.FloatField(label='Altura (m)')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'patient'
        if commit:
            user.save()
            profile = user.profile
            profile.birth_date = self.cleaned_data['birth_date']
            profile.save()
            Patient.objects.create(
                user=user,
                sex=self.cleaned_data['sex'],
                height=self.cleaned_data['height'],
            )
        return user


class NutriAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
