from django.urls import path
from . import views

app_name = 'examinations'

urlpatterns = [
    path('', views.exam_dashboard, name='dashboard'),
    path('exams/', views.exam_list, name='exams'),
    path('exams/add/', views.add_exam, name='add_exam'),
    path('exams/<int:pk>/', views.exam_detail, name='exam_detail'),
    path('exams/<int:pk>/enter-results/', views.enter_results, name='enter_results'),
]