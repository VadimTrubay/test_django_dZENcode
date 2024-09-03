from django.db import models
from django.utils import timezone

from app.users.models import CustomUser


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    file = models.FileField(upload_to="files/", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text[:20]
