from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('departments/', views.department_list, name='departments'),
    path('departments/add/', views.add_department, name='add_department'),
    path('subjects/', views.subject_list, name='subjects'),
    path('subjects/add/', views.add_subject, name='add_subject'),
    path('classes/', views.class_list, name='classes'),
    path('classes/add/', views.add_class, name='add_class'),
    path('timetable/', views.timetable_view, name='timetable'),
    path('timetable/add/', views.add_timetable, name='add_timetable'),
]
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('departments/', views.department_list, name='departments'),
    path('departments/add/', views.add_department, name='add_department'),
    path('subjects/', views.subject_list, name='subjects'),
    path('subjects/add/', views.add_subject, name='add_subject'),
    path('classes/', views.class_list, name='classes'),
    path('classes/add/', views.add_class, name='add_class'),
    path('timetable/', views.timetable_view, name='timetable'),
    path('timetable/add/', views.add_timetable, name='add_timetable'),
]