from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from tweet.forms import TweetForm
from tweet.models import Tweet
from twitteruser.models import TwitterUser
from notification.models import Notification

import re


class IndexView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        tweets = Tweet.objects.filter(
            user__in=request.user.following.all()).order_by('-date')
        user = request.user
        return render(request, "index.html", {"tweets": tweets, "user": user})


class TweetView(TemplateView):
    def get(self, request, tweet_id):
        tweet = Tweet.objects.get(id=tweet_id)
        return render(request, "tweet.html", {"tweet": tweet})


class AddTweetView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        form = TweetForm()
        return render(request, "generic_form.html", {"form": form})

    def post(self, request):
        form = TweetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            tweet = Tweet.objects.create(
                text=data.get('text'),
                user=request.user,
            )

            matches = re.findall(r"@\S+", tweet.text)
            if matches:
                for user in matches:
                    mentioned_user = TwitterUser.objects.get(username=user[1:])
                    if mentioned_user:
                        Notification.objects.create(
                            mentioned_user=mentioned_user,
                            tweet=tweet,
                        )

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "generic_form.html", {"form": form})
