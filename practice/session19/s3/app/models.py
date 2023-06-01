from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.


class Posts(models.Model):
   file = models.URLField(max_length=2000)  # Consider the maximum length required for your URLs


   def __str__(self):
       return self.file
