from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('reference_code', 'customer_name', 'business', 'service', 'staff_member', 'start_time', 'status')
    list_filter = ('status', 'business', 'service', 'staff_member')
    search_fields = ('reference_code', 'customer_name', 'customer_phone', 'customer_email',
                     'staff_member__name', 'service__name')
    readonly_fields = ('reference_code', 'created_at', 'updated_at')
    ordering = ('-start_time',)
    list_select_related = ('business', 'service', 'staff_member')
    list_editable = ('status',)
    date_hierarchy = 'start_time'
    fieldsets = (
        ('Customer', {'fields': ('customer_name', 'customer_phone', 'customer_email')}),
        ('Booking Details', {'fields': ('business', 'service', 'staff_member', 'start_time', 'end_time')}),
        ('Status & Notes', {'fields': ('status', 'notes', 'reference_code')}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )
