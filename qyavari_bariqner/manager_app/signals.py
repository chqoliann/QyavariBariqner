from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.utils import timezone

@receiver(user_logged_out)
def update_last_logout(sender, request, user, **kwargs):
    user.userprofile.last_logout = timezone.now()
    user.userprofile.save()
