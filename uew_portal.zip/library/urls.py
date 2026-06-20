from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.library_dashboard, name='dashboard'),
    path('books/', views.book_list, name='books'),
    path('books/add/', views.add_book, name='add_book'),
    path('borrow/', views.borrow_book, name='borrow'),
    path('records/', views.borrow_records, name='borrow_records'),
    path('return/<int:pk>/', views.return_book, name='return_book'),
]