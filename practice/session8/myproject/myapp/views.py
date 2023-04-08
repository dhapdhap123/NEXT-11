from django.shortcuts import render, redirect
from .models import Article, Comment

# Create your views here.
def new(request):    
    if request.method == 'POST':
        new_article = Article.objects.create(
            title = request.POST['title'],
            category = request.POST['category'],
            content = request.POST['content'],
        )
        return redirect('list')
    
    return render(request, 'new.html')

def list(request):
    articles = Article.objects.all()
    categories = []
    for i in articles:
        if i.category not in categories:
            categories.append(i.category)

    return render(request, 'list.html', {'articles': articles, 'categories': categories})

def detail(request, article_id):
    article = Article.objects.get(id = article_id)
    comments = Comment.objects.filter(parent_comment = None)
    recomments = Comment.objects.exclude(parent_comment = None).filter(article = article)

    return render(request, 'detail.html', {'article': article, 'comments': comments, 'recomments': recomments})

def category(request, category):
    articles = Article.objects.filter(category = category)
    return render(request, 'category.html', {'articles': articles, 'category': category})

def delete_comment(request, article_id, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    return redirect('detail', article_id)

def create_comment(request, article_id):
    if request.method == 'POST':
        article = Article.objects.get(id=article_id)
        content = request.POST['content']
        Comment.objects.create(
            article = article,
            content = content,
        )
        return redirect('detail', article_id)
    return render(request, 'detail.html', {'article': article})

def create_recomment(request, article_id, comment_id):
    article = Article.objects.get(pk=article_id)
    if request.method == 'POST':
        comment = Comment.objects.get(id = comment_id)
        content = request.POST['re_content']
        Comment.objects.create(
            article = article,
            content = content,
            parent_comment = comment
        )
        return redirect('detail', article_id)
    return render(request, 'detail.html', {'article': article})