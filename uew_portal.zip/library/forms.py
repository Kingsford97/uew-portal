from django import forms
from students.models import Student
from teachers.models import Teacher
from .models import Book, BorrowRecord


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'isbn', 'publisher', 'publication_year',
            'edition', 'category', 'quantity', 'available_quantity',
            'location', 'description', 'cover_image'
        ]
        widgets = {
            'publication_year': forms.NumberInput(attrs={'min': 1900, 'max': 2026}),
        }


class BorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['book', 'borrower_type', 'borrower_id', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_borrower_id(self):
        borrower_type = self.cleaned_data.get('borrower_type')
        borrower_id = self.cleaned_data.get('borrower_id')

        if borrower_type == 'student':
            if not Student.objects.filter(pk=borrower_id).exists():
                raise forms.ValidationError("Student not found!")
        else:
            if not Teacher.objects.filter(pk=borrower_id).exists():
                raise forms.ValidationError("Teacher not found!")

        return borrower_id


class ReturnForm(forms.Form):
    return_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    notes = forms.CharField(widget=forms.Textarea, required=False)