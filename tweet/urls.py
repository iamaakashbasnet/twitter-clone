from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='tweet-home'),
    path('about/', views.about, name='tweet-about')
]
