from django.urls import path

from auth import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('twofactor/', views.two_factor, name='two_factor'),
    path('qrcode/', views.qrcode, name='qrcode'),
]

app_name = 'auth'
