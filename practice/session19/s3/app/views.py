from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse
# from config.settings import (
#     AWS_ACCESS_KEY_ID,
#     AWS_SECRET_ACCESS_KEY,
#     AWS_STORAGE_BUCKET_NAME,
#     AWS_S3_IMAGE_URL,
# )
from uuid import uuid4
from app.models import Posts
import boto3
# Create your views here.
import os

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')


def write_task(request):
   get_file = request.FILES.get("get_file")
  
   if get_file:
       uuid_name = uuid4()
       image_datetime = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
       fileobj_key = str(uuid_name) + "_" + image_datetime
      
       s3_client = boto3.client(
           "s3",
           aws_access_key_id = AWS_ACCESS_KEY_ID,
           aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
       )
      
       s3_client.upload_fileobj(
           get_file,
           AWS_STORAGE_BUCKET_NAME,
           fileobj_key,
           ExtraArgs={
               "ContentType": get_file.content_type,
           },
       )
      
       image_url = fileobj_key
       image_src = os.environ.get('AWS_BUCKET_URL')+image_url
       Posts.objects.create(
           file=image_url,
       )
       return render(request, "result.html", {"image_url":image_url,"image_src":image_src})
  
   return render(request, "indexpy.html")


def index(request):
   return render(request, 'indexpy.html')
