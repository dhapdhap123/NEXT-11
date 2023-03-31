from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length = 200)
    category = models.CharField(null=True, max_length = 20)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title