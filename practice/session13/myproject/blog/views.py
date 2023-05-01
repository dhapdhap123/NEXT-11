from django.shortcuts import render, redirect
from .models import Post

# Create your views here.
def home(request):
    posts = Post.objects.all()

    return render(request, 'blog/home.html', {'posts': posts})

def new(request):
    if request.method == 'POST':
        new_post = Post.objects.create(
            title = request.POST['title'],
            content = request.POST['content'],
        )
        return redirect('blog:detail', new_post.pk)
    return render(request, 'blog/new.html')

def detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)

    return render(request, 'blog/detail.html', {'post': post})

def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST':
        Post.objects.filter(pk=post_pk).update(
            title = request.POST['title'],
            content = request.POST['content'],
        )
        return redirect('blog:detail', post_pk)
    
def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    post.delete()

    return redirect('blog:home')