from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from students.models import Student
from teachers.models import Teacher
from .models import Book, BorrowRecord
from .forms import BookForm, BorrowForm, ReturnForm


# ============ LIBRARY DASHBOARD ============

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


# ============ BOOK VIEWS ============

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


# ============ BORROW VIEWS ============

@login_required
def borrow_book(request):
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow = form.save()

            # Update book availability
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

            # Update book availability
            book = record.book
            book.available_quantity += 1
            book.save()

            messages.success(request, f'Book "{book.title}" returned successfully!')
            return redirect('library:borrow_records')
    else:
        form = ReturnForm()

    return render(request, 'library/return.html', {'form': form, 'record': record})