from django import forms
from .models import Department, Subject, Class, Timetable


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'head_of_department']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'description', 'department', 'teacher', 'credits']


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'code', 'department', 'class_teacher', 'academic_year', 'room_number', 'capacity']


class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['class_name', 'subject', 'teacher', 'day', 'start_time', 'end_time', 'room']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }