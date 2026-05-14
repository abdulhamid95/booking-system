from django.contrib import admin

from .models import StaffMember


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    pass
