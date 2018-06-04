from django.contrib import admin
from .models import Partograph, PartoMeasure


class MeasurementInline(admin.TabularInline):
    model = PartoMeasure
    extra = 0

# Register your models here.
class PartographAdmin(admin.ModelAdmin):
    model = Partograph
    inlines = [MeasurementInline]

# Register your models here.
class PartoMeasureAdmin(admin.ModelAdmin):
    model = PartoMeasure

admin.site.register(Partograph, PartographAdmin)
admin.site.register(PartoMeasure, PartoMeasureAdmin)