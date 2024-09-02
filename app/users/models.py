from django.db import models
from django.core.validators import EmailValidator, URLValidator


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(validators=[EmailValidator()])
    home_page = models.URLField(validators=[URLValidator()], blank=True, null=True)

    def __str__(self):
        return self.username
