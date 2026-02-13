from django.contrib import admin
from .models import (
    User, Bookings, Visitor, GamingStation, 
    Staff, Role, GamingZone, Shifts, Visits, Demo, WebsiteBooking
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'phone_number', 'data_joined')
    search_fields = ('full_name', 'email', 'phone_number')
    list_filter = ('data_joined',)
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'gaming_zone_id', 'guest_count', 'user_id', 'total_price')
    list_filter = ('gaming_zone_id',)
    search_fields = ('id',)
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(GamingZone)
class GamingZoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hourly_rate', 'specifications')
    search_fields = ('name', 'specifications')
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(GamingStation)
class GamingStationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    list_filter = ('status',)
    search_fields = ('name',)
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'last_activity', 'ip_address')
    list_filter = ('last_activity',)
    search_fields = ('ip_address',)
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'phone_number', 'role_id')
    search_fields = ('full_name', 'email', 'phone_number')
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'salary')
    search_fields = ('name',)
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(Shifts)
class ShiftsAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff_id', 'start_time', 'end_time')
    list_filter = ('start_time', 'end_time')
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(Visits)
class VisitsAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking_id', 'visitor_id', 'check_in_time', 'check_out_time')
    list_filter = ('check_in_time', 'check_out_time')
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(Demo)
class DemoAdmin(admin.ModelAdmin):
    list_display = ('id',)
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    from .models import WebsiteBooking

@admin.register(WebsiteBooking)
class WebsiteBookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'booking_date', 'booking_time', 'duration', 'guests', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('full_name', 'phone', 'email')
    list_editable = ('status',)
    ordering = ('-booking_date', '-booking_time')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Контактная информация', {
            'fields': ('full_name', 'phone', 'email')
        }),
        ('Детали бронирования', {
            'fields': ('booking_date', 'booking_time', 'duration', 'guests')
        }),
        ('Дополнительно', {
            'fields': ('comments', 'status', 'created_at')
        }),
    )