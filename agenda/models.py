from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from usuarios.models import Patient
from nutriFoco.models import BaseModel

User = settings.AUTH_USER_MODEL


class Availability(BaseModel):
    nutritionist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField(default=timezone.localdate)
    start_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nutritionist} - {self.date} {self.start_time}"


class Appointment(BaseModel):
    STATUS_CHOICES = (
        ('scheduled', 'Agendada'),
        ('confirmed', 'Confirmada'),
        ('canceled', 'Cancelada'),
        ('done', 'Realizada'),
        ('missed', 'Não compareceu'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    nutritionist = models.ForeignKey(User, on_delete=models.CASCADE)
    availability = models.OneToOneField(
        Availability,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointment',
    )

    datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    duration_minutes = models.PositiveIntegerField(default=60)
    notes = models.TextField(blank=True, null=True)

    def clean(self):
        if Appointment.objects.filter(
            nutritionist=self.nutritionist,
            datetime=self.datetime,
            deleted_at__isnull=True
        ).exclude(id=self.id).exists():
            raise ValidationError("Horário já ocupado")

    def __str__(self):
        return f"{self.patient} - {self.datetime}"


class ConsultationNote(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultation_notes')
    nutritionist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultation_notes')
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consultation_notes',
    )
    note_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Appointment.STATUS_CHOICES, default='scheduled')
    observations = models.TextField()

    def __str__(self):
        return f"{self.patient} - {self.note_datetime}"