from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.user_login, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.user_logout, name='logout'),
    path('upload/', views.upload, name='upload'),
    path('detail/', views.detail_custom, name='detail_custom'),
    path('edit/', views.edit_custom, name='edit_custom'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)