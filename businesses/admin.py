from django.contrib import admin

from .models import Business


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'business_type', 'phone', 'created_at')
    list_filter = ('business_type',)
    search_fields = ('name', 'owner__email', 'phone')
    ordering = ('name',)
    readonly_fields = ('created_at',)
    list_select_related = ('owner',)
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Basic Info', {'fields': ('owner', 'name', 'business_type')}),
        ('Contact', {'fields': ('phone', 'address')}),
        ('Metadata', {'fields': ('created_at',)}),
    )