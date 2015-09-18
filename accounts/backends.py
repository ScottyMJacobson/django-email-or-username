from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import check_password
from django.core.validators import validate_email
from django.forms import ValidationError

User = get_user_model()

class EmailOrUsernameAuthBackend():
    """
    A custom authentication backend. Allows users to log in using their email address or username.
    """

    def _lookup_user(self, username_or_email):
        try:
            validate_email(username_or_email)
        except ValidationError:
            # not an email
            using_email = False
        else:
            # looks like an email!
            using_email = True
        
        try:
            if using_email:
                user = User.objects.get(email__iexact=username_or_email)
            else:
                user = User.objects.get(username__iexact=username_or_email)
        except User.DoesNotExist:
            return None
        else:
            return user

    def authenticate(self, username=None, password=None):
        """
        Authentication method - username here is actually "username_or_email",
        but named as such to fit Django convention
        """
        user = self._lookup_user(username)

        if user:
            if user.check_password(password):
                return user

        return None
        

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None
