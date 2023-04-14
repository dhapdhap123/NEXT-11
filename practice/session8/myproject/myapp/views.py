from django.shortcuts import render, redirect
from .models import Article, Comment, Recomment

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        exist_user = User.objects.filter(username=username)

        if exist_user:
            error = "이미 존재하는 유저입니다."
            return render(request, 'registration/signup.html', {"error":error})

        new_user = User.objects.create_user(username=username, password=password)
        auth.login(request, new_user)
        return redirect('list')        

    return render(request, 'registration/signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(request.GET.get('next', '/'))
        else:
            error = '아이디 또는 비밀번호가 틀립니다'
            return render(request, 'registration/login.html', {'error': error})

    return render(request, 'registration/login.html')

def logout(request):
   auth.logout(request)
   return redirect('list')

@login_required(login_url="/registration/login/")
def new(request):
    if request.method == 'POST':
        new_article = Article.objects.create(
            title = request.POST['title'],
            category = request.POST['category'],
            content = request.POST['content'],
            author=request.user
        )
        return redirect('list')
    
    return render(request, 'new.html')

def edit_article(request, article_id):
    article = Article.objects.get(id=article_id)
    if request.method == 'POST':
        Article.objects.filter(pk = article_id).update(
            title = request.POST['title'],
            category = request.POST['category'],
            content = request.POST['content'],
            author=request.user
        )
        return redirect('detail', article_id)
    return render(request, 'edit_article.html', {'article': article})

def delete_article(request, article_id):
    article = Article.objects.get(id=article_id)
    if article.author == request.user:
        article.delete()
        return redirect('list')
    else:
        error = "자신의 게시글만 삭제할 수 있습니다."
        return redirect('detail_with_error', article_id=article_id, error=error)

def list(request):
    articles = Article.objects.all()
    return render(request, 'list.html', {'articles': articles})

@login_required(login_url="/registration/login/")
def detail(request, article_id, error=None):
    article = Article.objects.get(id = article_id)
    comments = Comment.objects.filter(article = article)
    recomments = Recomment.objects.all()

    if error:
        return render(request, 'detail.html', {'article': article, 'comments': comments, 'recomments': recomments, 'error': error})
    else:
        return render(request, 'detail.html', {'article': article, 'comments': comments, 'recomments': recomments})

def category(request, category):
    articles = Article.objects.filter(category = category)
    return render(request, 'category.html', {'articles': articles, 'category': category})

def create_comment(request, article_id):
    if request.method == 'POST':
        article = Article.objects.get(id=article_id)
        content = request.POST['content']
        Comment.objects.create(
            article = article,
            content = content,
            author=request.user
        )
        return redirect('detail', article_id)
    return render(request, 'detail.html', {'article': article})

def delete_comment(request, article_id, comment_id):
    article = Article.objects.get(id=article_id)
    if article.author == request.user:
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
        return redirect('detail', article_id)
    else:
        error = "자신의 댓글만 삭제할 수 있습니다."
        return redirect('detail_with_error', article_id=article_id, error=error)

def create_recomment(request, article_id, comment_id):
    article = Article.objects.get(pk=article_id)
    if request.method == 'POST':
        comment = Comment.objects.get(id = comment_id)
        content = request.POST['re_content']
        Recomment.objects.create(
            content = content,
            parent_comment = comment,
            author=request.user
        )
        return redirect('detail', article_id)
    return render(request, 'detail.html', {'article': article})

def delete_recomment(request, article_id, recomment_id):
    article = Article.objects.get(id=article_id)
    if article.author == request.user:
        recomment = Recomment.objects.get(id = recomment_id)
        recomment.delete()
        return redirect('detail', article_id)
    else:
        error = "자신의 대댓글만 삭제할 수 있습니다."
        return redirect('detail_with_error', article_id=article_id, error=error)