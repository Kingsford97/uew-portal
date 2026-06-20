from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='dashboard'),
    path('list/', views.teacher_list, name='list'),
    path('add/', views.add_teacher, name='add'),
    path('<int:pk>/', views.teacher_detail, name='detail'),
    path('attendance/', views.staff_attendance, name='attendance'),
    path('leave-requests/', views.leave_requests, name='leave_requests'),
]