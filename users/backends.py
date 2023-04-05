from django.contrib.auth.backends import ModelBackend as DefaultModelBackend
from pyisemail import is_email
from users import models
import re


class ModelBackend(DefaultModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return
        try:
            if is_email(address=username):
                user = models.User.objects.filter(email__exact=username).first()
            elif re.match(pattern=r"^9\d{9}$", string=username):
                user = models.User.objects.filter(phone__exact=username).first()
            else:
                return
        except models.User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            models.User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
