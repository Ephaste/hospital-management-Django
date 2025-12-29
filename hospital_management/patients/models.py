from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('admitted', 'Admitted'),
        ('outpatient', 'Outpatient'),
        ('discharged', 'Discharged'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='male'
    )

    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='outpatient'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
