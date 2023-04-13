from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length = 200)
    category = models.CharField(null=True, max_length = 20)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article', default=1)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', default=1)

    def __str__(self):
        return self.content
    
class Recomment(models.Model):
    content = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', default=1)
    
    def __str__(self):
        return self.content