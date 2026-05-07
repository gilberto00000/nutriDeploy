from django.contrib import admin

from .models import Appointment, Availability, ConsultationNote


admin.site.register(Appointment)
admin.site.register(Availability)
admin.site.register(ConsultationNote)