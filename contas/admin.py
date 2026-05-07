from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, User



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'user_type', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('Informações extras', {
            'fields': ('user_type',)
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações extras', {
            'fields': ('user_type',)
        }),
    )


admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cpf', 'phone', 'birth_date', 'crn', 'specialty')
    search_fields = ('user__username', 'cpf', 'crn')