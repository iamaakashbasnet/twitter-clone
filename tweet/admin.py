from django.contrib import admin
from .models import Tweet, Comment


# Register your models here.
admin.site.register(Tweet)
admin.site.register(Comment)
