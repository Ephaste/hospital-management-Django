from django.urls import path
from .views import account_creation, custom_login, custom_logout_view

urlpatterns = [
    path('register/', account_creation, name='register'),
    path('', custom_login, name='login'),
    path('logout/', custom_logout_view, name='logout'),
]
