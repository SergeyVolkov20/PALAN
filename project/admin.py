from django.contrib import admin
from .models import Car, Trip

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'license_plate', 'car_class', 'price_per_minute', 'fuel_level', 'is_available')
    list_filter = ('car_class', 'is_available')
    search_fields = ('model', 'license_plate')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('car', 'start_time', 'end_time', 'total_cost', 'is_active')
    list_filter = ('is_active',)