from django.shortcuts import render, redirect
from .models import Article, Comment

from django.contrib.auth.decorators import login_required

def home(request):
    articles = Article.objects.all()

    return render(request, 'blog/home.html', {'articles': articles})

@login_required
def detail(request, article_id, error=None):
    article = Article.objects.get(id=article_id)
    comments = Comment.objects.filter(article = article)

    if error:
        return render(request, 'blog/detail.html', {'article': article, 'comments': comments, 'error': error})
    else:
        return render(request, 'blog/detail.html', {'article': article, 'comments': comments})

@login_required
def create_article(request):
    if request.method == 'POST':
        new_article = Article.objects.create(
            title = request.POST['title'],
            content = request.POST['content'],
            author=request.user
        )
        return redirect('blog:detail', new_article.pk)

    return render(request, 'blog/create_article.html')

@login_required
def update_article(request, article_id):
    article = Article.objects.get(id=article_id)
    if article.author == request.user:
        if request.method == 'POST':
            article.title = request.POST['title']
            article.content = request.POST['content']
            article.save()
            return redirect('blog:detail', article_id=article_id)
        return render(request, 'blog/update_article.html', {'article': article})
    else:
        error = "자신의 게시글만 수정할 수 있습니다."
        return redirect('blog:detail_with_error', article_id=article_id, error=error)
    
@login_required
def delete_article(request, article_id):
    article = Article.objects.get(id=article_id)
    if article.author == request.user:
        article.delete()
        return redirect('blog:home')
    else:
        error = "자신의 게시글만 삭제할 수 있습니다."
        return redirect('blog:detail_with_error', article_id=article_id, error=error)

@login_required    
def create_comment(request, article_id):
    article = Article.objects.get(id=article_id)
    Comment.objects.create(
        content = request.POST['content'],
        author=request.user,
        article=article,
    )
    return redirect('blog:detail', article_id=article_id)

@login_required
def delete_comment(request, article_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.author == request.user:
        comment.delete()
        return redirect('blog:detail', article_id=article_id)
    else:
        error = "자신의 댓글만 삭제할 수 있습니다."
        return redirect('blog:detail_with_error', article_id=article_id, error=error)

@login_required    
def update_comment(request, article_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.author == request.user:
        if request.method == 'POST':
            comment.content = request.POST['content']
            comment.save()
            return redirect('blog:detail', article_id=article_id)
        return render(request, 'blog/update_comment.html', {'comment': comment})
    else:
        error = "자신의 댓글만 수정할 수 있습니다."
        return redirect('blog:detail_with_error', article_id=article_id, error=error)