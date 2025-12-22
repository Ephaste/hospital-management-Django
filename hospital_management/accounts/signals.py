from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from .models import RoleUser

User = get_user_model()

@receiver(post_save, sender=User)
def create_role_for_new_user(sender, instance, created, **kwargs):
    """
    Automatically create a RoleUser entry whenever a new User is created.
    Default role can be RECEPTIONIST for new users.
    """
    if created:
        RoleUser.objects.create(user=instance)
