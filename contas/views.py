from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView, TemplateView

from .mixins import PatientRequiredMixin
from .forms import NutriAuthenticationForm, NutritionistSignupForm, PatientSignupForm


class HomeView(TemplateView):
    template_name = 'contas/inicio.html'


class UserLoginView(LoginView):
    template_name = 'contas/entrar.html'
    authentication_form = NutriAuthenticationForm


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class NutritionistSignupView(CreateView):
    form_class = NutritionistSignupForm
    template_name = 'contas/cadastro.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cadastro de Nutricionista'
        return context


class PatientSignupView(CreateView):
    form_class = PatientSignupForm
    template_name = 'contas/cadastro.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cadastro de Cliente'
        return context


class DashboardRedirectView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('login')
        if self.request.user.user_type == 'nutritionist':
            return reverse_lazy('nutritionist_dashboard')
        return reverse_lazy('patient_limited_area')


class PatientLimitedAreaView(LoginRequiredMixin, PatientRequiredMixin, TemplateView):
    template_name = 'contas/area_restrita_paciente.html'
