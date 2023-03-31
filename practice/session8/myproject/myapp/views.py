from django.shortcuts import render, redirect
from .models import Article

# Create your views here.
def new(request):    
    if request.method == 'POST':

        print(request.POST)

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
    return render(request, 'detail.html', {'article': article})

def category(request, category):
    articles = Article.objects.filter(category = category)
    return render(request, 'category.html', {'articles': articles, 'category': category})