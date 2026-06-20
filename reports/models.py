from django.db import models
from django.contrib.auth.models import User


class Report(models.Model):
    REPORT_TYPES = [
        ('student', 'Student Report'),
        ('financial', 'Financial Report'),
        ('attendance', 'Attendance Report'),
        ('academic', 'Academic Report'),
        ('staff', 'Staff Report'),
        ('library', 'Library Report')
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    generated_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    data = models.JSONField(blank=True, null=True)
    file = models.FileField(upload_to='reports/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.generated_date}"