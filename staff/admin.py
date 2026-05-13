from django.contrib import admin

from .models import StaffMember


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'email', 'phone', 'is_active')
    list_filter = ('is_active', 'business')
    search_fields = ('name', 'email', 'business__name')
    list_editable = ('is_active',)
