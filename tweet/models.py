from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
class Tweet(models.Model):
    content = models.TextField(max_length=200, blank=False)
    image = models.ImageField(blank=True, null=True, upload_to='tweet_pics')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='likes')

    def __str__(self):
        return f'Post by { self.author } on { self.date_posted }'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 600 or img.width > 600:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def number_of_comments(self):
        return Comment.objects.filter(related_tweet=self).count()

    def get_absolute_url(self):
        return reverse('tweet-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    content = models.CharField(max_length=200, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    related_tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment on {self.related_tweet}'
