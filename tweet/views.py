from django.shortcuts import render
from .models import Tweet


# Create your views here.
def home(request):
    context = {
        'title': 'Home',
        'tweets': Tweet.objects.all()
    }
    return render(request, 'tweet/home.html', context)


def about(request):
    return render(request, 'tweet/about.html', {'title': 'About'})
