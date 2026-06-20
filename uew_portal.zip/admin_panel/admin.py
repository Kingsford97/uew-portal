from django.contrib import admin
from .models import DuesSettings, PaymentAccount, MemberVerification, PortalSettings, SystemLog


@admin.register(DuesSettings)
class DuesSettingsAdmin(admin.ModelAdmin):
    list_display = ['default_amount', 'due_date', 'academic_year', 'is_active']
    list_filter = ['is_active', 'academic_year']
    search_fields = ['academic_year']


@admin.register(PaymentAccount)
class PaymentAccountAdmin(admin.ModelAdmin):
    list_display = ['provider', 'account_number', 'account_name', 'is_active', 'is_default']
    list_filter = ['provider', 'is_active', 'is_default']
    search_fields = ['account_number', 'account_name', 'account_holder']


@admin.register(MemberVerification)
class MemberVerificationAdmin(admin.ModelAdmin):
    list_display = ['member', 'status', 'verified_date']
    list_filter = ['status']
    search_fields = ['member__first_name', 'member__last_name', 'member__student_id']
    readonly_fields = ['created_date']


@admin.register(PortalSettings)
class PortalSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'maintenance_mode']
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_logo', 'favicon', 'portal_profile_picture')
        }),
        ('Colors', {
            'fields': ('primary_color', 'secondary_color', 'accent_color')
        }),
        ('Footer', {
            'fields': ('footer_text',)
        }),
        ('Maintenance', {
            'fields': ('maintenance_mode', 'maintenance_message')
        }),
    )


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ['log_type', 'user', 'action', 'created_date']
    list_filter = ['log_type', 'created_date']
    search_fields = ['user__username', 'action']
    readonly_fields = ['created_date']