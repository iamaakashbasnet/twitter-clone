from django.shortcuts import render
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Tweet


# Create your views here.
# def home(request):
#     context = {
#         'title': 'Home',
#         'tweets': Tweet.objects.all()
#     }
#     return render(request, 'tweet/home.html', context)

class TweetListView(ListView):
    model = Tweet
    template_name = 'tweet/home.html'
    context_object_name = 'tweets'
    ordering = ['-date_posted']


class TweetDetailView(DetailView):
    model = Tweet


class TweetCreateView(LoginRequiredMixin, CreateView):
    model = Tweet
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TweetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tweet
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        Tweet = self.get_object()
        if self.request.user == Tweet.author:
            return True
        return False


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    success_url = '/'

    def test_func(self):
        Tweet = self.get_object()
        if self.request.user == Tweet.author:
            return True
        return False


def about(request):
    return render(request, 'tweet/about.html', {'title': 'About'})
