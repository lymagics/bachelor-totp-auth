from django.urls import path

from users import views

urlpatterns = [
    path('me/', views.user_get, name='me'),
]

app_name = 'users'
