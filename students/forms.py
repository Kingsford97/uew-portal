from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Avg
from .models import *
from .forms import *
from datetime import datetime

# ============ STUDENT VIEWS ============

@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
        context = {
            'student': student,
            'attendances': student.attendances.all()[:10],
            'records': student.academic_records.all()[:10],
            'total': Student.objects.count(),
            'active': Student.objects.filter(status='active').count(),
        }
        return render(request, 'students/dashboard.html', context)
    except Student.DoesNotExist:
        return render(request, 'students/no_profile.html')


@login_required
def student_list(request):
    students = Student.objects.all()
    context = {
        'students': students,
        'total': students.count(),
        'active': students.filter(status='active').count(),
        'graduated': students.filter(status='graduated').count(),
    }
    return render(request, 'students/list.html', context)


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    context = {
        'student': student,
        'attendances': student.attendances.all(),
        'academic_records': student.academic_records.all(),
        'payments': student.payments.all(),
    }
    return render(request, 'students/detail.html', context)


@login_required
def enroll_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username=username, password=password, email=email)
            student = form.save(commit=False)
            student.user = user
            student.save()
            messages.success(request, f'Student {student.full_name()} enrolled successfully!')
            return redirect('students:list')
    else:
        form = StudentForm()
    return render(request, 'students/enroll.html', {'form': form})


@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('students:detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/edit.html', {'form': form, 'student': student})


@login_required
def attendance_view(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance recorded successfully!')
            return redirect('students:attendance')
    else:
        form = AttendanceForm()
    attendances = Attendance.objects.all().order_by('-date')[:50]
    return render(request, 'students/attendance.html', {'form': form, 'attendances': attendances})


@login_required
def grades_view(request, pk=None):
    if pk:
        student = get_object_or_404(Student, pk=pk)
    else:
        student = get_object_or_404(Student, user=request.user)
    records = student.academic_records.all()
    context = {
        'student': student,
        'records': records,
        'total_subjects': records.count(),
        'average_score': records.aggregate(Avg('total_score'))['total_score__avg'],
    }
    return render(request, 'students/grades.html', context)


# ============ TEACHER VIEWS ============

@login_required
def teacher_dashboard(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        context = {
            'teacher': teacher,
            'attendances': teacher.attendances.all()[:10],
            'leave_requests': teacher.leave_requests.all()[:10],
            'total': Teacher.objects.count(),
            'active': Teacher.objects.filter(is_active=True).count(),
        }
        return render(request, 'teachers/dashboard.html', context)
    except Teacher.DoesNotExist:
        return render(request, 'teachers/no_profile.html')


@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    context = {
        'teachers': teachers,
        'total': teachers.count(),
        'active': teachers.filter(is_active=True).count(),
    }
    return render(request, 'teachers/list.html', context)


@login_required
def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'teachers/detail.html', {'teacher': teacher})


@login_required
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username=username, password=password, email=email)
            teacher = form.save(commit=False)
            teacher.user = user
            teacher.save()
            messages.success(request, f'Teacher {teacher.full_name()} added successfully!')
            return redirect('teachers:list')
    else:
        form = TeacherForm()
    return render(request, 'teachers/add.html', {'form': form})


@login_required
def staff_attendance(request):
    if request.method == 'POST':
        form = StaffAttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save()
            attendance.calculate_hours()
            messages.success(request, 'Staff attendance recorded successfully!')
            return redirect('teachers:attendance')
    else:
        form = StaffAttendanceForm()
    attendances = StaffAttendance.objects.all().order_by('-date')[:50]
    return render(request, 'teachers/attendance.html', {'form': form, 'attendances': attendances})


@login_required
def leave_requests(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.staff = Teacher.objects.get(user=request.user)
            leave.save()
            messages.success(request, 'Leave request submitted successfully!')
            return redirect('teachers:leave_requests')
    else:
        form = LeaveRequestForm()
    leaves = LeaveRequest.objects.all().order_by('-created_at')
    return render(request, 'teachers/leave_requests.html', {'form': form, 'leaves': leaves})


# ============ COURSE VIEWS ============

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'courses/departments.html', {'departments': departments})


@login_required
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully!')
            return redirect('courses:departments')
    else:
        form = DepartmentForm()
    return render(request, 'courses/add_department.html', {'form': form})


@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'courses/subjects.html', {'subjects': subjects})


@login_required
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject created successfully!')
            return redirect('courses:subjects')
    else:
        form = SubjectForm()
    return render(request, 'courses/add_subject.html', {'form': form})


@login_required
def class_list(request):
    classes = Class.objects.all()
    return render(request, 'courses/classes.html', {'classes': classes})


@login_required
def add_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class created successfully!')
            return redirect('courses:classes')
    else:
        form = ClassForm()
    return render(request, 'courses/add_class.html', {'form': form})


@login_required
def timetable_view(request):
    timetable = Timetable.objects.all()
    return render(request, 'courses/timetable.html', {'timetable': timetable})


@login_required
def add_timetable(request):
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Timetable entry created successfully!')
            return redirect('courses:timetable')
    else:
        form = TimetableForm()
    return render(request, 'courses/add_timetable.html', {'form': form})


# ============ FINANCE VIEWS ============

@login_required
def finance_dashboard(request):
    total_fees = StudentFee.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_paid - total_expenses
    context = {
        'total_fees': total_fees,
        'total_paid': total_paid,
        'total_expenses': total_expenses,
        'balance': balance,
        'pending_fees': StudentFee.objects.filter(status='pending').count(),
        'recent_payments': Payment.objects.all().order_by('-date')[:10],
        'recent_expenses': Expense.objects.all().order_by('-date')[:10],
    }
    return render(request, 'finance/dashboard.html', context)


@login_required
def fee_structure_list(request):
    fees = FeeStructure.objects.filter(is_active=True)
    return render(request, 'finance/fee_structure.html', {'fees': fees})


@login_required
def add_fee_structure(request):
    if request.method == 'POST':
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee structure added successfully!')
            return redirect('finance:fee_structure')
    else:
        form = FeeStructureForm()
    return render(request, 'finance/add_fee.html', {'form': form})


@login_required
def student_fees(request):
    student = Student.objects.get(user=request.user)
    fees = StudentFee.objects.filter(student=student)
    return render(request, 'finance/student_fees.html', {'fees': fees})


@login_required
def make_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.processed_by = request.user
            payment.save()
            fee = payment.fee
            fee.paid_amount += payment.amount
            fee.calculate_balance()
            messages.success(request, f'Payment of GHS {payment.amount} recorded successfully!')
            return redirect('finance:student_fees')
    else:
        form = PaymentForm()
    students = Student.objects.all()
    fees = StudentFee.objects.filter(status__in=['pending', 'partial'])
    return render(request, 'finance/make_payment.html', {'form': form, 'students': students, 'fees': fees})


@login_required
def expenses(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.created_by = request.user
            expense.save()
            messages.success(request, 'Expense recorded successfully!')
            return redirect('finance:expenses')
    else:
        form = ExpenseForm()
    expenses = Expense.objects.all().order_by('-date')
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'finance/expenses.html', {'form': form, 'expenses': expenses, 'total': total})


# ============ LIBRARY VIEWS ============

@login_required
def library_dashboard(request):
    total_books = Book.objects.count()
    available_books = Book.objects.aggregate(Sum('available_quantity'))['available_quantity__sum'] or 0
    borrowed_books = BorrowRecord.objects.filter(status='borrowed').count()
    overdue_books = BorrowRecord.objects.filter(status='overdue').count()
    context = {
        'total_books': total_books,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
        'overdue_books': overdue_books,
        'recent_borrows': BorrowRecord.objects.all().order_by('-borrow_date')[:10],
        'books': Book.objects.all()[:10],
    }
    return render(request, 'library/dashboard.html', context)


@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/books.html', {'books': books})


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('library:books')
    else:
        form = BookForm()
    return render(request, 'library/add_book.html', {'form': form})


@login_required
def borrow_book(request):
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow = form.save()
            book = borrow.book
            book.available_quantity -= 1
            book.save()
            messages.success(request, f'Book "{book.title}" borrowed successfully!')
            return redirect('library:borrow_records')
    else:
        form = BorrowForm()
    books = Book.objects.filter(available_quantity__gt=0)
    return render(request, 'library/borrow.html', {'form': form, 'books': books})


@login_required
def borrow_records(request):
    records = BorrowRecord.objects.all().order_by('-borrow_date')
    return render(request, 'library/borrow_records.html', {'records': records})


@login_required
def return_book(request, pk):
    record = get_object_or_404(BorrowRecord, pk=pk)
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            record.return_date = form.cleaned_data['return_date']
            record.status = 'returned'
            record.notes = form.cleaned_data['notes']
            record.save()
            book = record.book
            book.available_quantity += 1
            book.save()
            messages.success(request, f'Book "{book.title}" returned successfully!')
            return redirect('library:borrow_records')
    else:
        form = ReturnForm()
    return render(request, 'library/return.html', {'form': form, 'record': record})


# ============ EXAMINATION VIEWS ============

@login_required
def exam_dashboard(request):
    exams = Exam.objects.filter(is_active=True)
    results = ExamResult.objects.all()
    pass_rate = results.filter(is_passed=True).count() / results.count() * 100 if results.count() > 0 else 0
    context = {
        'total_exams': exams.count(),
        'total_results': results.count(),
        'pass_rate': pass_rate,
        'exams': exams[:10],
        'recent_results': results.order_by('-created_at')[:10],
    }
    return render(request, 'examinations/dashboard.html', context)


@login_required
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'examinations/exams.html', {'exams': exams})


@login_required
def add_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam created successfully!')
            return redirect('examinations:exams')
    else:
        form = ExamForm()
    return render(request, 'examinations/add_exam.html', {'form': form})@login_required
def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    results = exam.results.all()
    context = {
        'exam': exam,
        'results': results,
        'total_students': results.count(),
        'average_score': results.aggregate(Avg('marks_obtained'))['marks_obtained__avg'],
        'pass_count': results.filter(is_passed=True).count(),
    }
    return render(request, 'examinations/exam_detail.html', context)


@login_required
def enter_results(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    students = Student.objects.filter(student_class=exam.class_name)
    if request.method == 'POST':
        for student in students:
            marks = request.POST.get(f'marks_{student.id}')
            if marks:
                result, created = ExamResult.objects.get_or_create(
                    exam=exam, student=student,
                    defaults={'marks_obtained': marks}
                )
                if not created:
                    result.marks_obtained = marks
                    result.save()
                result.calculate_percentage()
                result.determine_grade()
        messages.success(request, 'Results entered successfully!')
        return redirect('examinations:exam_detail', pk=exam.pk)
    results = {r.student_id: r for r in exam.results.all()}
    return render(request, 'examinations/enter_results.html', {
        'exam': exam, 'students': students, 'results': results
    })


# ============ COMMUNICATION VIEWS ============

@login_required
def announcements(request):
    announcements = Announcement.objects.filter(is_published=True).order_by('-published_date')
    return render(request, 'communications/announcements.html', {'announcements': announcements})


@login_required
def add_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            messages.success(request, 'Announcement created successfully!')
            return redirect('communications:announcements')
    else:
        form = AnnouncementForm()
    return render(request, 'communications/add_announcement.html', {'form': form})


@login_required
def events(request):
    events = Event.objects.filter(is_active=True).order_by('date')
    return render(request, 'communications/events.html', {'events': events})


@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('communications:events')
    else:
        form = EventForm()
    return render(request, 'communications/add_event.html', {'form': form})


@login_required
def notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'communications/notifications.html', {
        'notifications': notifications, 'unread_count': unread_count
    })


@login_required
def send_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification sent successfully!')
            return redirect('communications:notifications')
    else:
        form = NotificationForm()
    return render(request, 'communications/send_notification.html', {'form': form})


@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.mark_as_read()
    return redirect('communications:notifications')


# ============ REPORT VIEWS ============

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