from django.shortcuts import render, redirect
from .models import Article, Comment, Profile, Image

from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required

from datetime import datetime
from uuid import uuid4
import boto3
from botocore.exceptions import ClientError
# Create your views here.
import os

import json
from django.core import serializers

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

def home(request):
    articles = Article.objects.all()

    sort_by = request.GET.get('sort_by', 'default_value')
    if sort_by == 'date':
        articles = Article.objects.all().order_by('create_dt')
    elif sort_by == 'reverse_date':
        articles = Article.objects.all().order_by('-create_dt')
    elif sort_by == 'title':
        articles = Article.objects.all().order_by('title')
    elif sort_by == 'reverse_title':
        articles = Article.objects.all().order_by('-title')
    return render(request, 'blog/home.html', {'articles': articles, 'sort_by': sort_by})

@login_required
def detail(request, article_id):
    article = Article.objects.get(id=article_id)
    comments = Comment.objects.filter(article = article)
    images = [image for image in Image.objects.filter(article = article)]

    error = None
    if 'error' in request.GET:
        error = request.GET['error']

    return render(request, 'blog/detail.html', {'article': article, 'comments': comments, 'images': images, 'error': error})

@login_required
def create_article(request):
    if request.method == 'POST':
        new_article = Article.objects.create(
            title = request.POST['title'],
            content = request.POST['content'],
            author = request.user
        )
        article_id = new_article.pk
        images = request.FILES.getlist('images')
        if images:
            for image in images:
                fileobj_key = create_uuidKey()
                s3_client = boto3.client(
                    "s3",
                    aws_access_key_id = AWS_ACCESS_KEY_ID,
                    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
                )
                create_image(s3_client, fileobj_key, image, new_article, request.user)
        response = {
            'article_id': article_id
        }

        return HttpResponse(json.dumps(response))
    return render(request, 'blog/create_article.html')

@login_required
def update_article(request, article_id):
    article = Article.objects.get(id=article_id)
    if article.author == request.user:
        images = Image.objects.filter(article = article)
        images_json = serializers.serialize('json', images)

        if request.method == 'POST':
            article.title = request.POST['title']
            article.content = request.POST['content']
            article.save()
            
            s3_client = boto3.client(
                "s3",
                aws_access_key_id = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
            )

            get_images = request.FILES.getlist('images')
            delete_images = request.POST.getlist('delete_images')
            if delete_images:
                for delete_image in delete_images:
                    s3_client.delete_object(
                        Bucket = AWS_STORAGE_BUCKET_NAME,
                        Key = delete_image
                    )
                    full_name = os.environ.get('AWS_BUCKET_URL')+delete_image
                    image = Image.objects.get(file=full_name)
                    image.delete()

            if get_images:
                
                for image in get_images:
                    try:
                        response = s3_client.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=str(image))
                    except ClientError as e:
                        fileobj_key = create_uuidKey()

                        if e.response['Error']['Code'] == 'NoSuchKey':
                            create_image(s3_client, fileobj_key, image, article, request.user)
            response = {
                'article_id': article_id
            }

            return HttpResponse(json.dumps(response))
            # return redirect('blog:detail', article_id=article_id)
        return render(request, 'blog/update_article.html', {'article': article, 'images': images_json})
    else:
        error = "자신의 게시글만 수정할 수 있습니다."
        redirect_url = f'/blog/detail/{article_id}/?error={error}'
        return redirect(redirect_url)
    
@login_required
def delete_article(request, article_id):
    article = Article.objects.get(id=article_id)
    if article.author == request.user:
        images = Image.objects.filter(article=article)
        s3_client = boto3.client(
            "s3",
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        )
        for image in images:
            s3_client.delete_object(
                Bucket = AWS_STORAGE_BUCKET_NAME,
                Key = image.file.replace(os.environ.get('AWS_BUCKET_URL'), '')
            )
        article.delete()
        return redirect('blog:home')
    else:
        error = "자신의 게시글만 삭제할 수 있습니다."
        redirect_url = f'/blog/detail/{article_id}/?error={error}'
        return redirect(redirect_url)

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
            redirect_url = f'/blog/detail/{article_id}/?error={error}'
            return redirect(redirect_url)

@login_required
def update_comment(request, article_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.author == request.user:
        if request.method == 'POST':
            comment.content = request.POST['content']
            comment.save()
            return redirect('blog:detail', article_id=article_id)
        return render(request, 'blog/update_comment.html', {'article_id':article_id, 'comment_id':comment_id, 'comment': comment})
    else:
        error = "자신의 댓글만 수정할 수 있습니다."
        redirect_url = f'/blog/detail/{article_id}/?error={error}'
        return redirect(redirect_url)

@login_required 
def author_article(request, author_id):
    author = Profile.objects.get(id=author_id)
    articles = Article.objects.filter(author=author)

    return render(request, 'blog/author_article.html', {'articles': articles, 'author': author})





def create_image(s3_client, fileobj_key, image, article, author):
    s3_client.upload_fileobj(
        image,
        AWS_STORAGE_BUCKET_NAME,
        fileobj_key,
        ExtraArgs={
            "ContentType": image.content_type,
        },
    )

    image_url = fileobj_key
    image_src = os.environ.get('AWS_BUCKET_URL')+image_url
    Image.objects.create(
        file = image_src,
        article = article,
        author = author
    )

def delete_image():
    return

def create_uuidKey():
    uuid_name = uuid4()
        
    image_datetime = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    fileobj_key = str(uuid_name) + "_" + image_datetime
    return fileobj_key