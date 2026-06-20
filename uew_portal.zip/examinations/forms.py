from django import forms
from .models import Exam, ExamResult


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = [
            'name', 'exam_type', 'subject', 'class_name',
            'date', 'start_time', 'duration', 'total_marks',
            'passing_marks', 'venue', 'invigilator'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class ExamResultForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = ['marks_obtained', 'remarks']