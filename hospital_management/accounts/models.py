# from django.db import models
# from django.contrib.auth.models import AbstractUser


# class CustomUser(AbstractUser):
#     ROLE_CHOICES = [
#         ("DOCTOR", "Doctor"),
#         ("NURSE", "Nurse"),
#         ("RECEPTIONIST", "Receptionist"),
#         ("PHARMACIST", "Pharmacist"),
#         ("ADMIN", "Admin"),
#     ]

#     role = models.CharField(
#         max_length=25,
#         choices=ROLE_CHOICES,
#         default="RECEPTIONIST"
#     )

#     def __str__(self):
#         return f"{self.username} ({self.role})"


import uuid
from datetime import datetime, timezone

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("user_type", User.ADMIN)

        return self.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields,
        )

class User(AbstractUser, PermissionsMixin):
    RECORDER = "RECORDER"
    SUPERVISOR = "SUPERVISOR"
    FINANCE = "FINANCE"
    ADMIN = "ADMIN"

    ROLE_CHOICES = [
        (RECORDER, "Recorder"),
        (SUPERVISOR, "Supervisor"),
        (FINANCE, "Finance"),
        (ADMIN, "Admin"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user_type = models.CharField(
        max_length=25,
        choices=ROLE_CHOICES,
        default=RECORDER,
    )

    email = models.EmailField(_("email address"), unique=True)

    phone_number = models.CharField(
        _("phone number"),
        max_length=13,
        unique=True,
        null=True,
        blank=True,
        validators=[
            MinLengthValidator(13),
            MaxLengthValidator(13),
        ],
    )

    is_first_login = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    def __str__(self):
        return f"{self.username} ({self.user_type})"


class VerificationCode(models.Model):
    SIGNUP = "SIGNUP"
    RESET_PASSWORD = "RESET_PASSWORD"
    CHANGE_EMAIL = "CHANGE_EMAIL"

    LABEL_CHOICES = [
        (SIGNUP, "Signup"),
        (RESET_PASSWORD, "Reset Password"),
        (CHANGE_EMAIL, "Change Email"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="verification_codes",
    )

    code = models.CharField(max_length=6)
    label = models.CharField(max_length=30, choices=LABEL_CHOICES, default=SIGNUP)
    is_pending = models.BooleanField(default=True)
    email = models.EmailField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("code", "user")

    def __str__(self):
        return f"{self.user.username} - {self.code}"

    @property
    def is_valid(self):
        expiry_time = self.created_on + settings.VERIFICATION_CODE_LIFETIME
        return datetime.now(timezone.utc) < expiry_time

