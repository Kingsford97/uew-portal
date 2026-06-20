from django.urls import path
from .import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('add-member/', views.add_member, name='add_member'),
    path('manage-dues/', views.manage_dues, name='manage_dues'),
    path('manage-payment-accounts/', views.manage_payment_accounts, name='manage_payment_accounts'),
    path('verify-member/<int:member_id>/', views.verify_member, name='verify_member'),
    path('upload-portal-picture/', views.upload_portal_picture, name='upload_portal_picture'),
    path('member-list/', views.member_list, name='member_list'),
]