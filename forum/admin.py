from django.contrib import admin
from .models import Category, UploadItem, Message, Comment
from django.contrib.auth.models import User

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)

@admin.register(UploadItem)
class UploadItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'created_at', 'read')
    list_filter = ('read', 'created_at')
    search_fields = ('subject', 'message', 'user__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('post__title', 'user__username', 'text')
