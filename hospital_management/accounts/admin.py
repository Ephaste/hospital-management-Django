from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, VerificationCode


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    # Show these columns in admin list view
    list_display = (
        "username",
        "email",
        "user_type",
        "is_active",
        "is_staff",
        "is_admin",
    )

    list_filter = ("user_type", "is_active", "is_staff")

    # Add custom fields to the edit page
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Hospital Role & Extra Info",
            {
                "fields": (
                    "user_type",
                    "phone_number",
                    "is_first_login",
                    "is_admin",
                )
            },
        ),
    )

    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "email", "code", "label", "is_pending", "created_on")
    list_filter = ("label", "is_pending")
    search_fields = ("email", "code")
