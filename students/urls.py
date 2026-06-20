from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('list/', views.student_list, name='list'),
    path('enroll/', views.enroll_student, name='enroll'),
    path('<int:pk>/', views.student_detail, name='detail'),
    path('<int:pk>/edit/', views.edit_student, name='edit'),
    path('<int:pk>/grades/', views.grades_view, name='grades'),
    path('attendance/', views.attendance_view, name='attendance'),
]