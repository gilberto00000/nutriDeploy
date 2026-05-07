from django.contrib import admin
from .models import Patient, Progress, Food, NutritionPlan, Meal, DailyLog


admin.site.register(Patient)
admin.site.register(Progress)
admin.site.register(Food)
admin.site.register(NutritionPlan)
admin.site.register(Meal)
admin.site.register(DailyLog)