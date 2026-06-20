from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.finance_dashboard, name='dashboard'),
    path('fee-structure/', views.fee_structure_list, name='fee_structure'),
    path('fee-structure/add/', views.add_fee_structure, name='add_fee'),
    path('student-fees/', views.student_fees, name='student_fees'),
    path('make-payment/', views.make_payment, name='make_payment'),
    path('expenses/', views.expenses, name='expenses'),
]