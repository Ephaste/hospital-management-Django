from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Adds your custom field "role" to the admin edit page
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

    # Columns displayed in the admin list view
    list_display = ['username', 'email', 'role', 'is_staff']
