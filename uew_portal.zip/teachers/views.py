from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Teacher, StaffAttendance, LeaveRequest
from .forms import TeacherForm, StaffAttendanceForm, LeaveRequestForm
from django.db.models import Count


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
            'on_leave': LeaveRequest.objects.filter(status='approved').count(),
            'departments': Department.objects.count() if 'Department' in globals() else 0,
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