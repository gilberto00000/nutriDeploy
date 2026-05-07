from django.urls import path

from .views import (
    AppointmentCreateView,
    AppointmentStatusUpdateView,
    AvailabilityCreateView,
    AvailabilityDeleteView,
    AvailabilityListView,
    AvailabilityUpdateView,
    ConsultationNoteCreateView,
    ConsultationNoteDeleteView,
    ConsultationNoteListView,
    ConsultationNoteUpdateView,
    NutritionistDashboardView,
    NutritionistAppointmentListView,
    PatientAppointmentListView,
)

urlpatterns = [
    path('dashboard/', NutritionistDashboardView.as_view(), name='nutritionist_dashboard'),
    path('disponibilidades/', AvailabilityListView.as_view(), name='availability_list'),
    path('disponibilidades/nova/', AvailabilityCreateView.as_view(), name='availability_create'),
    path('disponibilidades/<int:pk>/editar/', AvailabilityUpdateView.as_view(), name='availability_update'),
    path('disponibilidades/<int:pk>/excluir/', AvailabilityDeleteView.as_view(), name='availability_delete'),
    path('consultas/agendar/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('consultas/nutricionista/', NutritionistAppointmentListView.as_view(), name='nutritionist_appointments'),
    path('consultas/cliente/', PatientAppointmentListView.as_view(), name='patient_appointments'),
    path('consultas/<int:pk>/status/', AppointmentStatusUpdateView.as_view(), name='appointment_status_update'),
    path('notas/', ConsultationNoteListView.as_view(), name='consultation_note_list'),
    path('notas/nova/', ConsultationNoteCreateView.as_view(), name='consultation_note_create'),
    path('notas/<int:pk>/editar/', ConsultationNoteUpdateView.as_view(), name='consultation_note_update'),
    path('notas/<int:pk>/excluir/', ConsultationNoteDeleteView.as_view(), name='consultation_note_delete'),
]
