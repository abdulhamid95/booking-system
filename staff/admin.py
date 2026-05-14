from django.contrib import admin

from .models import StaffMember


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'email', 'phone', 'is_active')
    list_filter = ('is_active', 'business')
    search_fields = ('name', 'email', 'phone', 'business__name')
    ordering = ('business', 'name')
    filter_horizontal = ('services',)
    list_select_related = ('business',)
    list_editable = ('is_active',)
    fieldsets = (
        ('Basic Info', {'fields': ('business', 'name')}),
        ('Contact', {'fields': ('email', 'phone')}),
        ('Services & Status', {'fields': ('is_active', 'services')}),
    )
