from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required

from tweet.forms import TweetForm
from tweet.models import Tweet


@login_required
def index(request):
    return render(request, "index.html")


def add_tweet_view(request):
    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            tweet = Tweet.objects.create(
                text=data.get('text'),
                user=request.user,
            )
            return HttpResponseRedirect(reverse("index"))

    form = TweetForm()
    return render(request, "generic_form.html", {"form": form})
