from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from students.models import Student
from .models import FeeStructure, StudentFee, Payment, Expense
from .forms import FeeStructureForm, StudentFeeForm, PaymentForm, ExpenseForm


# ============ FINANCE DASHBOARD ============

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


# ============ FEE STRUCTURE VIEWS ============

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


# ============ STUDENT FEES VIEWS ============

@login_required
def student_fees(request):
    try:
        student = Student.objects.get(user=request.user)
        fees = StudentFee.objects.filter(student=student)
        return render(request, 'finance/student_fees.html', {'fees': fees})
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('member_dashboard')


# ============ PAYMENT VIEWS ============

@login_required
def make_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.processed_by = request.user
            payment.save()

            # Update student fee
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


# ============ EXPENSE VIEWS ============

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