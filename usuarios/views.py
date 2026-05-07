from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, ListView, UpdateView, TemplateView
)

from .models import Agendamento
from .forms import AgendamentoForm

from contas.mixins import NutritionistRequiredMixin, PatientRequiredMixin
from .models import NutritionPlan, Patient, DailyLog
from .forms import NutritionPlanForm, DailyLogForm


# NUTRICIONISTA

class NutritionPlanListView(LoginRequiredMixin, NutritionistRequiredMixin, ListView):
    model = NutritionPlan
    template_name = 'usuarios/planos_alimentares_lista.html'
    context_object_name = 'plans'
    paginate_by = 8

    def get_queryset(self):
        queryset = NutritionPlan.objects.filter(
            nutritionist=self.request.user
        ).select_related('patient', 'patient__user').order_by('-start_date')

        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(patient__user__first_name__icontains=query) |
                Q(patient__user__username__icontains=query)
            )
        return queryset


class NutritionPlanCreateView(LoginRequiredMixin, NutritionistRequiredMixin, CreateView):
    model = NutritionPlan
    form_class = NutritionPlanForm
    template_name = 'usuarios/plano_alimentar_formulario.html'
    success_url = reverse_lazy('nutrition_plan_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['patient'].queryset = Patient.objects.filter(
            Q(nutritionist=self.request.user) | Q(nutritionist__isnull=True)
        ).select_related('user')
        return form

    def form_valid(self, form):
        form.instance.nutritionist = self.request.user
        patient = form.cleaned_data['patient']

        if patient.nutritionist_id is None:
            patient.nutritionist = self.request.user
            patient.save(update_fields=['nutritionist'])

        return super().form_valid(form)


class NutritionPlanUpdateView(LoginRequiredMixin, NutritionistRequiredMixin, UpdateView):
    model = NutritionPlan
    form_class = NutritionPlanForm
    template_name = 'usuarios/plano_alimentar_formulario.html'
    success_url = reverse_lazy('nutrition_plan_list')

    def get_queryset(self):
        return NutritionPlan.objects.filter(nutritionist=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['patient'].queryset = Patient.objects.filter(
            nutritionist=self.request.user
        )
        return form


class NutritionPlanDeleteView(LoginRequiredMixin, NutritionistRequiredMixin, DeleteView):
    model = NutritionPlan
    template_name = 'shared/confirmar_exclusao.html'
    success_url = reverse_lazy('nutrition_plan_list')

    def get_queryset(self):
        return NutritionPlan.objects.filter(nutritionist=self.request.user)


# PACIENTE

class DashboardPacienteView(LoginRequiredMixin, PatientRequiredMixin, TemplateView):
    template_name = 'usuarios/dashboard_paciente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        patient = Patient.objects.get(user=self.request.user)

        context['plans'] = NutritionPlan.objects.filter(
            patient=patient,
            active=True
        ).order_by('-start_date')

        context['logs'] = DailyLog.objects.filter(
            patient=patient
        ).order_by('-date')[:5]

        return context


class DailyLogCreateView(LoginRequiredMixin, PatientRequiredMixin, CreateView):
    model = DailyLog
    form_class = DailyLogForm
    template_name = 'usuarios/registro_diario_form.html'
    success_url = reverse_lazy('dashboard_paciente')

    def form_valid(self, form):
        patient = Patient.objects.get(user=self.request.user)
        form.instance.patient = patient
        return super().form_valid(form)


class DailyLogListView(LoginRequiredMixin, PatientRequiredMixin, ListView):
    model = DailyLog
    template_name = 'usuarios/registros_lista.html'
    context_object_name = 'logs'

    def get_queryset(self):
        patient = Patient.objects.get(user=self.request.user)
        return DailyLog.objects.filter(
            patient=patient
        ).order_by('-date')
    
class AgendamentoCreateView(LoginRequiredMixin, PatientRequiredMixin, CreateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'usuarios/agendamento_form.html'
    success_url = reverse_lazy('agendamento_list')

    def form_valid(self, form):
        disponibilidade = form.cleaned_data['disponibilidade']

        form.instance.patient = self.request.user.patient
        form.instance.nutritionist = disponibilidade.nutritionist
        form.instance.data = disponibilidade.date
        form.instance.hora = disponibilidade.start_time

        disponibilidade.is_available = False
        disponibilidade.save()

        return super().form_valid(form)

class AgendamentoListView(LoginRequiredMixin, PatientRequiredMixin, ListView):
    model = Agendamento
    template_name = 'usuarios/agendamentos_lista.html'
    context_object_name = 'agendamentos'

    def get_queryset(self):
        return Agendamento.objects.filter(
            patient=self.request.user.patient
        ).order_by('-data')