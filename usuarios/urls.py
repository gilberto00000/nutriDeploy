from django.urls import path
from .views import AgendamentoCreateView, AgendamentoListView
from .views import (
    DashboardPacienteView,
    NutritionPlanCreateView,
    NutritionPlanDeleteView,
    NutritionPlanListView,
    NutritionPlanUpdateView,
    DailyLogCreateView,
    DailyLogListView,
)

urlpatterns = [
     # NUTRICIONISTA
    path('planos/', NutritionPlanListView.as_view(), name='nutrition_plan_list'),
    path('planos/novo/', NutritionPlanCreateView.as_view(), name='nutrition_plan_create'),
    path('planos/<int:pk>/editar/', NutritionPlanUpdateView.as_view(), name='nutrition_plan_update'),
    path('planos/<int:pk>/excluir/', NutritionPlanDeleteView.as_view(), name='nutrition_plan_delete'),

    # PACIENTE
    path('cliente/area/', DashboardPacienteView.as_view(), name='dashboard_paciente'),
    path('cliente/diario/', DailyLogListView.as_view(), name='lista_registros'),
    path('cliente/diario/novo/', DailyLogCreateView.as_view(), name='novo_registro'),
    path('registros/', DailyLogListView.as_view(), name='daily_log_list'),
    path('registros/novo/', DailyLogCreateView.as_view(), name='daily_log_create'),
    path('agendar/', AgendamentoCreateView.as_view(), name='agendamento_create'),
    path('meus-agendamentos/', AgendamentoListView.as_view(), name='agendamento_list'),
]
