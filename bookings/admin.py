from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('reference_code', 'customer_name', 'business', 'service', 'staff_member', 'start_time', 'status')
    list_filter = ('status', 'business', 'service')
    search_fields = ('reference_code', 'customer_name', 'customer_phone', 'customer_email')
    readonly_fields = ('reference_code', 'created_at', 'updated_at')
    ordering = ('-start_time',)
