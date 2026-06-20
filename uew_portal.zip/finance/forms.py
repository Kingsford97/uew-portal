from django import forms
from .models import FeeStructure, StudentFee, Payment, Expense


class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['name', 'description', 'amount', 'academic_year']


class StudentFeeForm(forms.ModelForm):
    class Meta:
        model = StudentFee
        fields = ['student', 'fee_structure', 'amount', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'fee', 'amount', 'payment_method', 'reference', 'notes']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'category', 'amount', 'date', 'receipt', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }