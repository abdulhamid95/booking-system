from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'duration_minutes', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'business')
    search_fields = ('name', 'business__name')
    ordering = ('business', 'name')
    readonly_fields = ('created_at',)
    list_select_related = ('business',)
    list_editable = ('is_active', 'price')
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Basic Info', {'fields': ('business', 'name', 'description')}),
        ('Pricing & Duration', {'fields': ('price', 'duration_minutes')}),
        ('Status', {'fields': ('is_active',)}),
        ('Metadata', {'fields': ('created_at',)}),
    )
