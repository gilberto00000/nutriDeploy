from django.urls import path

from .views import (
    DashboardRedirectView,
    HomeView,
    PatientLimitedAreaView,
    NutritionistSignupView,
    PatientSignupView,
    UserLoginView,
    UserLogoutView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('cadastro/nutricionista/', NutritionistSignupView.as_view(), name='signup_nutritionist'),
    path('cadastro/cliente/', PatientSignupView.as_view(), name='signup_patient'),
    path('dashboard/', DashboardRedirectView.as_view(), name='dashboard_redirect'),
    path('cliente/area/', PatientLimitedAreaView.as_view(), name='patient_limited_area'),
]
