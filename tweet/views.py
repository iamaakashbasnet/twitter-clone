from django.shortcuts import render, get_object_or_404
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
from django.contrib.auth.models import User
from .models import Tweet, Comment
from users.models import Follow
from .forms import NewCommentForm


# Create your views here.
# def home(request):
#     context = {
#         'title': 'Home',
#         'tweets': Tweet.objects.all()
#     }
#     return render(request, 'tweet/home.html', context)

def is_users(post_user, logged_user):
    return post_user == logged_user


class TweetListView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = 'tweet/home.html'
    context_object_name = 'tweets'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        qs = Follow.objects.filter(user=user)
        follows = [user]
        for obj in qs:
            follows.append(obj.follow_user)
        return Tweet.objects.filter(author__in=follows).order_by('-date_posted')


class TweetDetailView(DetailView):
    model = Tweet

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        related_comments = Comment.objects.filter(
            related_tweet=self.get_object()).order_by('-date_posted')
        data['comments'] = related_comments
        data['form'] = NewCommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),
                              author=self.request.user,
                              related_tweet=self.get_object())
        new_comment.save()

        return self.get(self, request, *args, **kwargs)


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


class UserTweetListView(ListView):
    model = Tweet
    template_name = 'tweet/user_tweets.html'
    context_object_name = 'tweets'
    paginate_by = 5

    def tweet_author(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        logged_user = self.request.user
        tweet_author = self.tweet_author()
        if logged_user.username == '' or logged_user is None:
            can_follow = False
        else:
            can_follow = (Follow.objects.filter(user=logged_user,
                                                follow_user=tweet_author).count() == 0)
        data = super().get_context_data(**kwargs)
        data['author_profile'] = tweet_author
        data['can_follow'] = can_follow
        return data

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Tweet.objects.filter(author=user).order_by('-date_posted')

    def post(self, request, *args, **kwargs):
        if request.user.id is not None:
            follows_between = Follow.objects.filter(user=request.user,
                                                    follow_user=self.tweet_author())

            if 'follow' in request.POST:
                new_relation = Follow(
                    user=request.user, follow_user=self.tweet_author())
                if follows_between.count() == 0:
                    new_relation.save()
            elif 'unfollow' in request.POST:
                if follows_between.count() > 0:
                    follows_between.delete()

        return self.get(self, request, *args, **kwargs)


def about(request):
    return render(request, 'tweet/about.html', {'title': 'About'})
