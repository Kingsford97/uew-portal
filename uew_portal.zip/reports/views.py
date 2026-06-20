from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg
from students.models import Student, Attendance, StudentAcademicRecord
from finance.models import Payment, Expense
from library.models import BorrowRecord, Book
from teachers.models import Teacher


@login_required
def report_dashboard(request):
    return render(request, 'reports/dashboard.html')


@login_required
def student_report(request):
    total_students = Student.objects.count()
    active_students = Student.objects.filter(status='active').count()
    by_class = Student.objects.values('student_class__name').annotate(count=Count('id'))
    by_gender = Student.objects.values('gender').annotate(count=Count('id'))

    context = {
        'total_students': total_students,
        'active_students': active_students,
        'by_class': by_class,
        'by_gender': by_gender,
    }
    return render(request, 'reports/student_report.html', context)


@login_required
def financial_report(request):
    total_payments = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_payments - total_expenses

    by_method = Payment.objects.values('payment_method').annotate(total=Sum('amount'))
    by_month = Payment.objects.values('date__month').annotate(total=Sum('amount'))

    context = {
        'total_payments': total_payments,
        'total_expenses': total_expenses,
        'balance': balance,
        'by_method': by_method,
        'by_month': by_month,
    }
    return render(request, 'reports/financial_report.html', context)


@login_required
def attendance_report(request):
    total_attendances = Attendance.objects.count()
    present = Attendance.objects.filter(status='present').count()
    absent = Attendance.objects.filter(status='absent').count()
    late = Attendance.objects.filter(status='late').count()
    attendance_rate = (present / total_attendances * 100) if total_attendances > 0 else 0

    context = {
        'total_attendances': total_attendances,
        'present': present,
        'absent': absent,
        'late': late,
        'attendance_rate': attendance_rate,
    }
    return render(request, 'reports/attendance_report.html', context)


@login_required
def academic_report(request):
    total_records = StudentAcademicRecord.objects.count()
    average_score = StudentAcademicRecord.objects.aggregate(Avg('total_score'))['total_score__avg'] or 0

    grade_distribution = {}
    for grade in ['A', 'B', 'C', 'D', 'F']:
        grade_distribution[grade] = StudentAcademicRecord.objects.filter(grade=grade).count()

    context = {
        'total_records': total_records,
        'average_score': average_score,
        'grade_distribution': grade_distribution,
    }
    return render(request, 'reports/academic_report.html', context)


@login_required
def library_report(request):
    total_books = Book.objects.count()
    total_borrows = BorrowRecord.objects.count()
    active_borrows = BorrowRecord.objects.filter(status='borrowed').count()
    overdue = BorrowRecord.objects.filter(status='overdue').count()
    popular_books = BorrowRecord.objects.values('book__title').annotate(total=Count('id')).order_by('-total')[:10]

    context = {
        'total_books': total_books,
        'total_borrows': total_borrows,
        'active_borrows': active_borrows,
        'overdue': overdue,
        'popular_books': popular_books,
    }
    return render(request, 'reports/library_report.html', context)