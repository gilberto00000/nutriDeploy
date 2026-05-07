from django import forms
from django.utils import timezone

from usuarios.models import Patient
from .models import Appointment, Availability, ConsultationNote


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['date', 'start_time', 'duration_minutes', 'is_available']
        labels = {
            'date': 'Data',
            'start_time': 'Horario de inicio',
            'duration_minutes': 'Duracao (minutos)',
            'is_available': 'Disponivel para agendamento',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class AppointmentCreateForm(forms.ModelForm):
    availability = forms.ModelChoiceField(
        queryset=Availability.objects.none(),
        label='Horario disponivel',
    )

    class Meta:
        model = Appointment
        fields = ['availability']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['availability'].queryset = Availability.objects.filter(
            is_available=True,
            date__gte=timezone.localdate(),
        ).order_by('date', 'start_time')


class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status', 'notes']
        labels = {
            'status': 'Status',
            'notes': 'Observacoes',
        }
        widgets = {'notes': forms.Textarea(attrs={'rows': 4})}


class ConsultationNoteForm(forms.ModelForm):
    class Meta:
        model = ConsultationNote
        fields = ['patient', 'appointment', 'note_datetime', 'status', 'observations']
        labels = {
            'patient': 'Paciente',
            'appointment': 'Consulta',
            'note_datetime': 'Data e hora',
            'status': 'Status',
            'observations': 'Observacoes',
        }
        widgets = {
            'note_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'observations': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, nutritionist=None, **kwargs):
        super().__init__(*args, **kwargs)
        if nutritionist:
            self.fields['patient'].queryset = Patient.objects.filter(nutritionist=nutritionist).select_related('user')
            self.fields['appointment'].queryset = Appointment.objects.filter(
                nutritionist=nutritionist
            ).select_related('patient__user')
