from django.db import models
from django.contrib.auth.models import User
from students.models import Student, Teacher


class DuesSettings(models.Model):
    """Settings for association dues"""
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_dues_settings')
    default_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateTimeField()
    academic_year = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dues: {self.default_amount} (Due: {self.due_date})"

    class Meta:
        ordering = ['-created_date']


class PaymentAccount(models.Model):
    """Payment accounts for receiving dues"""
    PAYMENT_PROVIDERS = [
        ('mobile_money', 'Mobile Money'),
        ('bank', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('other', 'Other')
    ]

    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_payment_accounts')
    provider = models.CharField(max_length=50, choices=PAYMENT_PROVIDERS, default='mobile_money')
    account_number = models.CharField(max_length=50)
    account_name = models.CharField(max_length=200)
    account_holder = models.CharField(max_length=200, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_provider_display()} - {self.account_number} ({self.account_name})"

    class Meta:
        ordering = ['-is_default', '-created_date']


class MemberVerification(models.Model):
    """Track member verification requests"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    member = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='verifications')
    admin_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='admin_verifications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    verified_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member} - {self.status}"

    class Meta:
        ordering = ['-created_date']
        verbose_name_plural = "Member Verifications"


class PortalSettings(models.Model):
    """Portal-wide settings"""
    site_name = models.CharField(max_length=100, default='UEW School Management System')
    site_logo = models.ImageField(upload_to='portal/', blank=True, null=True)
    favicon = models.ImageField(upload_to='portal/', blank=True, null=True)
    portal_profile_picture = models.ImageField(upload_to='portal/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, default='#1a237e')
    secondary_color = models.CharField(max_length=7, default='#0d47a1')
    accent_color = models.CharField(max_length=7, default='#1976d2')
    footer_text = models.CharField(max_length=200, default='© 2026 UEW School Management System')
    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name_plural = "Portal Settings"


class SystemLog(models.Model):
    """System activity logs"""
    LOG_TYPES = [
        ('login', 'Login'),('logout', 'Logout'),
        ('registration', 'Registration'),
        ('payment', 'Payment'),
        ('verification', 'Verification'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('error', 'Error'),
        ('other', 'Other')
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='system_logs')
    log_type = models.CharField(max_length=20, choices=LOG_TYPES)
    action = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_log_type_display()} - {self.user} - {self.created_date}"

    class Meta:
        ordering = ['-created_date']