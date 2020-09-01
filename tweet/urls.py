from django.urls import path
from django.conf.urls import url
from .views import (
    TweetListView,
    TweetDetailView,
    TweetCreateView,
    TweetUpdateView,
    TweetDeleteView,
    UserTweetListView
)
from . import views

urlpatterns = [
    path('', TweetListView.as_view(), name='tweet-home'),
    path('tweet/<int:pk>/', TweetDetailView.as_view(), name='tweet-detail'),
    path('tweet/new/', TweetCreateView.as_view(), name='tweet-create'),
    path('tweet/<int:pk>/update/', TweetUpdateView.as_view(), name='tweet-update'),
    path('tweet/<int:pk>/delete/', TweetDeleteView.as_view(), name='tweet-delete'),
    path('user/<str:username>', UserTweetListView.as_view(), name='user-tweets'),
    url(r'^like/$', views.like_button, name='like'),
    path('about/', views.about, name='tweet-about'),
]
