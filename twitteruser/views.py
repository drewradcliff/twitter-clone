from django.shortcuts import render

from twitteruser.models import TwitterUser
from tweet.models import Tweet


def user_view(request, user_id):
    user = TwitterUser.objects.get(id=user_id)
    tweets = Tweet.objects.filter(user=user_id)
    return render(request, "user.html", {"user": user, "tweets": tweets})
