from django.contrib import admin
from .models import User, Practitioner, Patient


class PatientAdmin(admin.ModelAdmin):
    model = Patient

class PractitionerAdmin(admin.ModelAdmin):
    model = Practitioner

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'patient', 'practitioner']})
    ]

admin.site.register(User, UserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Practitioner, PractitionerAdmin)