from django.contrib import admin
from .models import Article, Comment

class CommentInline(admin.TabularInline):
    model = Comment

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'create_dt', 'get_comments')
    inlines = [
        CommentInline,
    ]

    def get_comments(self, obj):
        return ", ".join([c.content for c in obj.comments.all()])
    
    get_comments.short_description = 'Comments'

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)