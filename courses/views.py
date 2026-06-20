from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Department, Subject, Class, Timetable
from .forms import DepartmentForm, SubjectForm, ClassForm, TimetableForm

# ============ DEPARTMENT VIEWS ============

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


# ============ SUBJECT VIEWS ============

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


# ============ CLASS VIEWS ============

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


# ============ TIMETABLE VIEWS ============

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