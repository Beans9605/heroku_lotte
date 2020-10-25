from django.urls.conf import path
from . import views

urlpatterns =[
    path('', views.clothHome, name="clothHome"),
    path('select/<int:pk>', views.selectCloth, name="selectCloth"),
    path('qrcode/', views.qr_code_authenticate, name="qrcode_auth"),
    # path('test', views.test_image, name='test'),
] 


