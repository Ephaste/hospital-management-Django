from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.account_creation, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('activate-account/', views.activate_account, name='activate-account'), 
]
