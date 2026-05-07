from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class NutritionistRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 'nutritionist'

    def handle_no_permission(self):
        raise PermissionDenied("Acesso exclusivo para nutricionistas.")


class PatientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 'patient'

    def handle_no_permission(self):
        raise PermissionDenied("Acesso exclusivo para clientes.")
