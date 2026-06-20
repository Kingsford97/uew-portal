from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_dashboard, name='dashboard'),
    path('student/', views.student_report, name='student'),
    path('financial/', views.financial_report, name='financial'),
    path('attendance/', views.attendance_report, name='attendance'),
    path('academic/', views.academic_report, name='academic'),
    path('library/', views.library_report, name='library'),
]