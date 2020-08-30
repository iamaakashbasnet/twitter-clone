from django.shortcuts import render


# Create your views here.
tweets = [
    {
        'author': 'Steve Smith',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]


def home(request):
    context = {
        'title': 'Home',
        'tweets': tweets
    }
    return render(request, 'tweet/home.html', context)


def about(request):
    return render(request, 'tweet/about.html', {'title': 'About'})
