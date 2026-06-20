from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from datetime import datetime


class MemberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')

    # Personal Details
    name = models.CharField(max_length=200)
    course = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    index_number = models.CharField(max_length=20, unique=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])],
        null=True,
        blank=True
    )

    # Association Details
    department_association = models.CharField(max_length=200)
    position = models.CharField(max_length=100, default='Member')

    # Payment Status
    has_paid_dues = models.BooleanField(default=False)
    dues_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, default='Mobile Money')
    payment_reference = models.CharField(max_length=100, blank=True, null=True)

    # Verification
    is_verified = models.BooleanField(default=False)
    verified_date = models.DateTimeField(null=True, blank=True)

    # Portal Profile Picture (from admin)
    portal_profile_picture = models.ImageField(
        upload_to='portal_pics/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])],
        null=True,
        blank=True
    )

    # Registration Date
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.index_number}"

    def is_profile_complete(self):
        return all([
            self.name,
            self.course,
            self.department,
            self.index_number,
            self.profile_picture,
            self.department_association,
            self.position
        ])

    class Meta:
        ordering = ['-registration_date']


class PaymentAccount(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_accounts')
    provider = models.CharField(max_length=50, default='Mobile Money')
    account_number = models.CharField(max_length=20)
    account_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider} - {self.account_number}"


class DuesSettings(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    default_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dues: {self.default_amount} (Due: {self.due_date})"