from django.db import models
from django.core.validators import EmailValidator, URLValidator
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(validators=[EmailValidator()], unique=True)
    home_page = models.URLField(validators=[URLValidator()], blank=True, null=True)

    def __str__(self):
        return self.username
