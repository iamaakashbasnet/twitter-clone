from django.contrib.auth.models import User


def sidebar_data(request):
    return {
        'new_users': User.objects.all().order_by('-id')[:5]
    }
