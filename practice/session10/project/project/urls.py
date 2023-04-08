from django.contrib import admin
from django.urls import path
from app import views


urlpatterns = [
   path('admin/', admin.site.urls),
   path('', views.home, name='home'),
   path('new/', views.new, name='new'),
   path('detail/<int:post_pk>', views.detail, name='detail'),
   path('edit/<int:post_pk>', views.edit, name='edit'),
   path('delete/<int:post_pk>', views.delete, name='delete'),
   path('delete-comment/<int:post_pk>/<int:comment_pk>',views.delete_comment, name='delete-comment'),
]
