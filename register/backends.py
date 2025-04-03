from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to fetch the user by email
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                # If no user is found by email, try to fetch by username
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None