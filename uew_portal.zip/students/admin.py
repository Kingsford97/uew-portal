from django.contrib import admin
from .models import *

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'student_class', 'status', 'is_verified']
    list_filter = ['status', 'gender', 'student_class', 'is_verified']
    search_fields = ['student_id', 'first_name', 'last_name', 'email', 'phone_number']
    list_per_page = 20

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'time_in', 'time_out']
    list_filter = ['status', 'date']
    search_fields = ['student__first_name', 'student__last_name']

@admin.register(StudentAcademicRecord)
class StudentAcademicRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'total_score', 'grade', 'term']
    list_filter = ['grade', 'term', 'academic_year']
    search_fields = ['student__first_name', 'student__last_name', 'subject__name']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher_id', 'first_name', 'last_name', 'qualification', 'employment_status', 'is_active']
    list_filter = ['employment_status', 'gender', 'is_active']
    search_fields = ['teacher_id', 'first_name', 'last_name', 'email', 'phone_number']
    list_per_page = 20

@admin.register(StaffAttendance)
class StaffAttendanceAdmin(admin.ModelAdmin):
    list_display = ['staff', 'date', 'status', 'check_in', 'check_out', 'hours_worked']
    list_filter = ['status', 'date']
    search_fields = ['staff__first_name', 'staff__last_name']

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['staff', 'leave_type', 'start_date', 'end_date', 'status']
    list_filter = ['leave_type', 'status']
    search_fields = ['staff__first_name', 'staff__last_name']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'head_of_department']
    search_fields = ['name', 'code']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'department', 'teacher', 'credits']
    list_filter = ['department']
    search_fields = ['name', 'code']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'department', 'class_teacher', 'current_students', 'capacity']
    list_filter = ['department', 'is_active']
    search_fields = ['name', 'code']

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['class_name', 'subject', 'teacher', 'day', 'start_time', 'end_time']
    list_filter = ['day', 'is_active']
    search_fields = ['class_name__name', 'subject__name']

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'academic_year', 'is_active']
    list_filter = ['is_active', 'academic_year']
    search_fields = ['name']

@admin.register(StudentFee)
class StudentFeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_structure', 'amount', 'paid_amount', 'balance', 'status']
    list_filter = ['status']
    search_fields = ['student__first_name', 'student__last_name']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount', 'payment_method', 'date', 'reference']
    list_filter = ['payment_method', 'date']
    search_fields = ['student__first_name', 'student__last_name', 'reference']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['description', 'category', 'amount', 'date']
    list_filter = ['category', 'date']
    search_fields = ['description']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'quantity', 'available_quantity', 'category']
    list_filter = ['category']
    search_fields = ['title', 'author', 'isbn']

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['book', 'borrower_type', 'borrow_date', 'due_date', 'status', 'fine_amount']
    list_filter = ['status', 'borrower_type']
    search_fields = ['book__title']

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'subject', 'class_name', 'date', 'total_marks']
    list_filter = ['exam_type', 'is_active']
    search_fields = ['name', 'subject__name']

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'marks_obtained', 'percentage', 'grade', 'is_passed']
    list_filter = ['grade', 'is_passed']
    search_fields = ['student__first_name', 'student__last_name']

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'is_published', 'created_at']
    list_filter = ['priority', 'is_published']
    search_fields = ['title', 'content']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'venue', 'organizer', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'venue']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'title', 'is_read', 'created_at']
    list_filter = ['is_read']
    search_fields = ['recipient__username', 'title']

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'generated_by', 'generated_date']
    list_filter = ['report_type']
    search_fields = ['title']