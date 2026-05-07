from django.db import models
from django.conf import settings
from nutriFoco.models import BaseModel
from django.utils import timezone


User = settings.AUTH_USER_MODEL


class Patient(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nutritionist = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='patients',
        null=True,
        blank=True,
    )

    SEX_CHOICES = (
        ('F', 'Feminino'),
        ('M', 'Masculino'),
        ('O', 'Outro'),
    )
    height = models.FloatField() 
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='O')
    initial_weight = models.FloatField(null=True, blank=True)
    goal = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.user}"


class Progress(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='progress')

    date = models.DateField(auto_now_add=True)
    weight = models.FloatField()
    imc = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.patient.height:
            self.imc = self.weight / (self.patient.height ** 2)
        super().save(*args, **kwargs)


class Food(BaseModel):
    name = models.CharField(max_length=100)
    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()

    def __str__(self):
        return self.name


class NutritionPlan(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='plans')
    nutritionist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='nutrition_plans',
        null=True,
        blank=True,
    )
    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(default=timezone.localdate)
    plan_text = models.TextField(
        help_text='Estruture o plano com horarios. Ex: 07:00 - Cafe da manha...',
        default='',
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Plano - {self.patient}"


class Meal(BaseModel):
    plan = models.ForeignKey(NutritionPlan, on_delete=models.CASCADE, related_name='meals')

    name = models.CharField(max_length=50)
    time = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.plan}"


class MealFood(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='foods')
    food = models.ForeignKey(Food, on_delete=models.CASCADE)

    quantity = models.FloatField()  

    def __str__(self):
        return f"{self.food} - {self.quantity}g"

class Agendamento(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    nutritionist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    data = models.DateField()
    hora = models.TimeField()

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.data} {self.hora}"
    
    

class DailyLog(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='logs')

    date = models.DateField()
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    followed = models.BooleanField()

    def __str__(self):
        return f"{self.patient} - {self.date}"
    