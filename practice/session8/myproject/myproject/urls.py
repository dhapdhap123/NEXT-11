"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.list, name='home'),
    path('list/', views.list, name='list'),
    path('new/', views.new, name='new'),
    path("delete_article/<int:article_id>/", views.delete_article, name="delete_article"),
    path("edit_article/<int:article_id>/", views.edit_article, name="edit_article"),
    path('detail/<int:article_id>', views.detail, name='detail'),
    path('category/<str:category>', views.category, name='category'),
    path('delete-comment/<int:article_id>/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('create_comment/<int:article_id>', views.create_comment, name='create_comment'),
    path('create_recomment/<int:article_id>/<int:comment_id>', views.create_recomment, name='create_recomment'),
    path('delete_recomment/<int:article_id>/<int:comment_id>', views.delete_recomment, name='delete_recomment'),
    path("registration/signup/", views.signup, name="signup"),
    path("registration/login/", views.login, name="login"),
    path("registration/logout/", views.logout, name="logout"),
    
]
