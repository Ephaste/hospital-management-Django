from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("DOCTOR", "Doctor"),
        ("NURSE", "Nurse"),
        ("RECEPTIONIST", "Receptionist"),
        ("PHARMACIST", "Pharmacist"),
        ("ADMIN", "Admin"),
    ]

    role = models.CharField(
        max_length=25,
        choices=ROLE_CHOICES,
        default="RECEPTIONIST"
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
