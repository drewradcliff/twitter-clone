from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from authentication.forms import LoginForm, SignupForm
from twitteruser.models import TwitterUser


class LoginView(TemplateView):
    def get(self, request):
        form = LoginForm()
        return render(request, "generic_form.html", {"form": form, "login": True})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get(
                "username"), password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse("index")))
        else:
            render(request, "generic_form.html", {"form": form, "login": True})


class SignupView(TemplateView):
    def get(self, request):
        form = SignupForm()
        return render(request, "generic_form.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = TwitterUser.objects.create_user(
                username=data.get("username"),
                password=data.get("password"),
            )
            user = TwitterUser.objects.filter(id=new_user.id)
            new_user.following.set(user)
            if new_user:
                login(request, new_user)
                return HttpResponseRedirect(reverse("index"))
        else:
            render(request, "generic_form.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))
