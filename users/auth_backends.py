from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if not user.check_password(password):
            # Increment the failed login attempts counter
            failed_attempts = user.failed_login_attempts
            last_failed_attempt = user.last_failed_attempt
            now = timezone.now()

            if not last_failed_attempt:
                # Set the last failed attempt timestamp on first failed attempt
                user.failed_login_attempts = 1
                user.last_failed_attempt = now
                user.save()
            elif last_failed_attempt and now - last_failed_attempt > timedelta(hours=1):
                # Reset the failed attempts counter and last failed attempt timestamp
                user.failed_login_attempts = 2
                user.last_failed_attempt = now
                user.save()
            elif failed_attempts >= 5:
                if now - last_failed_attempt < timedelta(minutes=1):
                    raise ValidationError(
                        'Too many failed login attempts. Please try again in 1 minute.')
                else:
                    # Reset the failed attempts counter and update the last failed attempt timestamp
                    user.failed_login_attempts = 1
                    user.last_failed_attempt = now
                    user.save()
            else:
                # Increment the failed attempts counter
                user.failed_login_attempts = failed_attempts + 1
                user.save()

            return None

        # Reset the failed attempts counter and last failed attempt timestamp on successful login
        user.failed_login_attempts = 0
        user.last_failed_attempt = None
        user.save()

        return user
