from django.db import models
from django.contrib.auth.models import User
from students.models import Student
from teachers.models import Teacher


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    publisher = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    edition = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    available_quantity = models.IntegerField(default=1)
    location = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def is_available(self):
        return self.available_quantity > 0


class BorrowRecord(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
        ('lost', 'Lost')
    ]
    BORROWER_TYPES = [
        ('student', 'Student'),
        ('teacher', 'Teacher')
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_records')
    borrower_type = models.CharField(max_length=20, choices=BORROWER_TYPES)
    borrower_id = models.IntegerField()
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='borrowed')
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.book} - {self.borrower_type} - {self.status}"

    def calculate_fine(self):
        from datetime import date
        if self.status == 'overdue' and not self.return_date:
            days_overdue = (date.today() - self.due_date).days
            if days_overdue > 0:
                self.fine_amount = days_overdue * 5
                self.save()
        return self.fine_amount

    def get_borrower_name(self):
        if self.borrower_type == 'student':
            try:
                student = Student.objects.get(pk=self.borrower_id)
                return student.full_name()
            except Student.DoesNotExist:
                return "Unknown Student"
        else:
            try:
                teacher = Teacher.objects.get(pk=self.borrower_id)
                return teacher.full_name()
            except Teacher.DoesNotExist:
                return "Unknown Teacher"