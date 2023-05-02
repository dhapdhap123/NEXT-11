from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('detail/<int:article_id>', views.detail, name='detail'),
    path('detail/<int:article_id>/<str:error>/', views.detail, name='detail_with_error'),
    
    path('create_article/', views.create_article, name='create_article'),
    path('update_article/<int:article_id>', views.update_article, name='update_article'),
    path('delete_article/<int:article_id>', views.delete_article, name='delete_article'),

    path('create_comment/<int:article_id>', views.create_comment, name='create_comment'),
    path('update_comment/<int:article_id>/<int:comment_id>', views.update_comment, name='update_comment'),
    path('delete_comment/<int:article_id>/<int:comment_id>', views.delete_comment, name='delete_comment'),
]