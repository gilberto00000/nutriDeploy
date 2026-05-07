from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from contas.mixins import NutritionistRequiredMixin, PatientRequiredMixin
from usuarios.models import Patient
from .forms import (
    AppointmentCreateForm,
    AppointmentStatusForm,
    AvailabilityForm,
    ConsultationNoteForm,
)
from .models import Appointment, Availability, ConsultationNote

from usuarios.models import Agendamento


class NutritionistDashboardView(LoginRequiredMixin, NutritionistRequiredMixin, TemplateView):
    template_name = 'agenda/painel_nutricionista.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        hoje = timezone.localdate()

        context['appointments_today'] = Agendamento.objects.filter(
            nutritionist=self.request.user,
            data=hoje
        ).order_by('hora')

        context['next_appointments'] = Agendamento.objects.filter(
            nutritionist=self.request.user,
            data__gt=hoje
        ).order_by('data', 'hora')

        context['next_slots'] = Availability.objects.filter(
            nutritionist=self.request.user,
            is_available=True,
            date__gte=hoje
        ).order_by('date', 'start_time')

        return context

class AvailabilityListView(LoginRequiredMixin, NutritionistRequiredMixin, ListView):
    model = Availability
    template_name = 'agenda/disponibilidades_lista.html'
    context_object_name = 'availabilities'
    paginate_by = 10

    def get_queryset(self):
        return Availability.objects.filter(nutritionist=self.request.user).order_by('date', 'start_time')


class AvailabilityCreateView(LoginRequiredMixin, NutritionistRequiredMixin, CreateView):
    model = Availability
    form_class = AvailabilityForm
    template_name = 'agenda/disponibilidade_formulario.html'
    success_url = reverse_lazy('availability_list')

    def form_valid(self, form):
        form.instance.nutritionist = self.request.user
        return super().form_valid(form)


class AvailabilityUpdateView(LoginRequiredMixin, NutritionistRequiredMixin, UpdateView):
    model = Availability
    form_class = AvailabilityForm
    template_name = 'agenda/disponibilidade_formulario.html'
    success_url = reverse_lazy('availability_list')

    def get_queryset(self):
        return Availability.objects.filter(nutritionist=self.request.user)


class AvailabilityDeleteView(LoginRequiredMixin, NutritionistRequiredMixin, DeleteView):
    model = Availability
    template_name = 'shared/confirmar_exclusao.html'
    success_url = reverse_lazy('availability_list')

    def get_queryset(self):
        return Availability.objects.filter(nutritionist=self.request.user)


class AppointmentCreateView(LoginRequiredMixin, PatientRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentCreateForm
    template_name = 'agenda/consulta_formulario.html'
    success_url = reverse_lazy('patient_appointments')

    def form_valid(self, form):
        availability = form.cleaned_data['availability']
        patient = Patient.objects.get(user=self.request.user)
        appointment_datetime = datetime.combine(availability.date, availability.start_time)
        form.instance.patient = patient
        form.instance.nutritionist = availability.nutritionist
        form.instance.availability = availability
        form.instance.datetime = appointment_datetime
        form.instance.duration_minutes = availability.duration_minutes
        response = super().form_valid(form)
        availability.is_available = False
        availability.save(update_fields=['is_available'])
        return response


class NutritionistAppointmentListView(LoginRequiredMixin, NutritionistRequiredMixin, ListView):
    model = Appointment
    template_name = 'agenda/consultas_lista_nutricionista.html'
    context_object_name = 'appointments'
    paginate_by = 10

    def get_queryset(self):
        return Appointment.objects.filter(nutritionist=self.request.user).select_related(
            'patient', 'patient__user'
        ).order_by('-datetime')


class PatientAppointmentListView(LoginRequiredMixin, PatientRequiredMixin, ListView):
    model = Appointment
    template_name = 'agenda/consultas_lista_paciente.html'
    context_object_name = 'appointments'
    paginate_by = 10

    def get_queryset(self):
        return Appointment.objects.filter(patient__user=self.request.user).select_related(
            'nutritionist'
        ).order_by('-datetime')


class AppointmentStatusUpdateView(LoginRequiredMixin, NutritionistRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentStatusForm
    template_name = 'agenda/status_consulta_formulario.html'
    success_url = reverse_lazy('nutritionist_appointments')

    def get_queryset(self):
        return Appointment.objects.filter(nutritionist=self.request.user)


class ConsultationNoteListView(LoginRequiredMixin, NutritionistRequiredMixin, ListView):
    model = ConsultationNote
    template_name = 'agenda/notas_consulta_lista.html'
    context_object_name = 'notes'
    paginate_by = 10

    def get_queryset(self):
        return ConsultationNote.objects.filter(nutritionist=self.request.user).select_related(
            'patient', 'patient__user'
        ).order_by('-note_datetime')


class ConsultationNoteCreateView(LoginRequiredMixin, NutritionistRequiredMixin, CreateView):
    model = ConsultationNote
    form_class = ConsultationNoteForm
    template_name = 'agenda/nota_consulta_formulario.html'
    success_url = reverse_lazy('consultation_note_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['nutritionist'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.nutritionist = self.request.user
        return super().form_valid(form)


class ConsultationNoteUpdateView(LoginRequiredMixin, NutritionistRequiredMixin, UpdateView):
    model = ConsultationNote
    form_class = ConsultationNoteForm
    template_name = 'agenda/nota_consulta_formulario.html'
    success_url = reverse_lazy('consultation_note_list')

    def get_queryset(self):
        return ConsultationNote.objects.filter(nutritionist=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['nutritionist'] = self.request.user
        return kwargs


class ConsultationNoteDeleteView(LoginRequiredMixin, NutritionistRequiredMixin, DeleteView):
    model = ConsultationNote
    template_name = 'shared/confirmar_exclusao.html'
    success_url = reverse_lazy('consultation_note_list')

    def get_queryset(self):
        return ConsultationNote.objects.filter(nutritionist=self.request.user)
