from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),        # This includes register/login/logout
    # path('dashboard/', include('dashboard.urls')),  # Optional: your dashboard app URLs
]
