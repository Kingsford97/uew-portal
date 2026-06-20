from django.db import models
from courses.models import Subject, Class
from students.models import Student
from teachers.models import Teacher


class Exam(models.Model):
    EXAM_TYPES = [
        ('mid_term', 'Mid Term'),
        ('end_term', 'End Term'),
        ('final', 'Final'),
        ('quiz', 'Quiz'),
        ('mock', 'Mock')
    ]

    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    total_marks = models.IntegerField()
    passing_marks = models.IntegerField()
    venue = models.CharField(max_length=100)
    invigilator = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.date})"


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_results')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grade = models.CharField(max_length=2, blank=True)
    is_passed = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_percentage(self):
        self.percentage = (self.marks_obtained / self.exam.total_marks) * 100
        self.save()
        return self.percentage

    def determine_grade(self):
        if self.percentage >= 80:
            self.grade = 'A'
            self.is_passed = True
        elif self.percentage >= 70:
            self.grade = 'B'
            self.is_passed = True
        elif self.percentage >= 60:
            self.grade = 'C'
            self.is_passed = True
        elif self.percentage >= 50:
            self.grade = 'D'
            self.is_passed = True
        else:
            self.grade = 'F'
            self.is_passed = False
        self.save()
        return self.grade

    def __str__(self):
        return f"{self.student} - {self.exam} - {self.grade}"