from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Tweet(models.Model):
    content = models.CharField(max_length=200, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Post by { self.author } on { self.date_posted }'
