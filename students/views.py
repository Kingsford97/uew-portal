from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Avg
from .models import *
from .forms import *

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