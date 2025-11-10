from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserSession
from django.utils import timezone


@receiver(user_logged_in)
def create_user_session(sender, request, user, **kwargs):
    UserSession.objects.create(user=user, login_time=timezone.now())
    
    
@receiver(user_logged_out)
def update_user_session(sender, request, user, **kwargs):
    last_session = UserSession.objects.filter(user=user, logout_time__isnull=True).last()
    if last_session:
        last_session.logout_time = timezone.now()
        last_session.save()