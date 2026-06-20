from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from members import views as member_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', member_views.login_view, name='home'),
    path('signup/', member_views.signup, name='signup'),
    path('login/', member_views.login_view, name='login'),
    path('logout/', member_views.logout_view, name='logout'),
    path('dashboard/', member_views.member_dashboard, name='member_dashboard'),
    path('profile-setup/', member_views.profile_setup, name='profile_setup'),
    path('upload-picture/', member_views.upload_profile_picture, name='upload_picture'),
    path('update-details/', member_views.update_member_details, name='update_details'),
    path('pay-dues/', member_views.pay_dues, name='pay_dues'),

    # Admin URLs
    path('admin-panel/', include('admin_panel.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)