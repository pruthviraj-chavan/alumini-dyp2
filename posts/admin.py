from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    """Admin interface for Post model"""
    list_display = ('title', 'category', 'user', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Post, PostAdmin)
