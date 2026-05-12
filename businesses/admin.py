from django.contrib import admin

from .models import Business


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'business_type', 'phone', 'created_at')
    list_filter = ('business_type',)
    search_fields = ('name', 'owner__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)