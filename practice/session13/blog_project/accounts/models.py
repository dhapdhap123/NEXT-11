from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Profile(AbstractUser):
    # add custom fields
    bio = models.TextField(max_length=500, blank=True, null=True)