from django.urls import path
from . import views

app_name = 'communications'

urlpatterns = [
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/add/', views.add_announcement, name='add_announcement'),
    path('events/', views.events, name='events'),
    path('events/add/', views.add_event, name='add_event'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/send/', views.send_notification, name='send_notification'),
    path('notifications/read/<int:pk>/', views.mark_notification_read, name='mark_read'),
]