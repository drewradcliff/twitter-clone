from django.db import models
from django.contrib.auth.models import AbstractUser


class TwitterUser(AbstractUser):
    display_name = models.CharField(max_length=240)
