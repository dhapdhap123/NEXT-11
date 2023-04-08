from django.db import models


class Post(models.Model):
   title = models.CharField(max_length=50)
   content = models.TextField()


   def __str__(self):
       return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, related_name="comments", null=True)
    content = models.TextField(null=True)

    def __str__(self):
        return self.content