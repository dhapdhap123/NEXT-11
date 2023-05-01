from django.contrib import admin
from blog.models import Post, Comment

# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'create_dt']
    list_display_links = ['id', 'title']
    list_filter = ['create_dt', 'author']
    search_fields = ['tilte', 'author']
    inlines = [
        CommentInline,
    ]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'content', 'author')