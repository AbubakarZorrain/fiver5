from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from customers.models import User
from customers.utilities import get_company


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        company = get_company(request)
        if company is None:
            return None
        else:
            try:
             user = User.objects.get(email=username, company=company)
             if user is None:
                 return None
             else:
                 valid = user.check_password(password)
                 if valid:
                     return user
            except User.DoesNotExist:
                return None
