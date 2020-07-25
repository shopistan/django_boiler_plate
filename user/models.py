"""
 User App models Here
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

class User(AbstractUser):
    """
     User Model
    """
    username = models.CharField(blank=True, null=True, max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = "user"

    def __str__(self):
        return "{}".format(self.email)
