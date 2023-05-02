from django.db import models
from accounts.models import Profile

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField()
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='article', default=1)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments', default=1)
    create_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content