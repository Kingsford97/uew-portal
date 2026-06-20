# teachers/models.py
# This file re-exports models from students/models.py

from students.models import Teacher, StaffAttendance, LeaveRequest

# Also import other models that might be needed
from students.models import (
    Student, Attendance, StudentAcademicRecord,
    Department, Subject, Class, Timetable,
    FeeStructure, StudentFee, Payment, Expense,
    Book, BorrowRecord,
    Exam, ExamResult,
    Announcement, Event, Notification,
    Report
)

# Make all models available at the module level
all = [
    'Teacher', 'StaffAttendance', 'LeaveRequest',
    'Student', 'Attendance', 'StudentAcademicRecord',
    'Department', 'Subject', 'Class', 'Timetable',
    'FeeStructure', 'StudentFee', 'Payment', 'Expense',
    'Book', 'BorrowRecord',
    'Exam', 'ExamResult',
    'Announcement', 'Event', 'Notification',
    'Report'
]