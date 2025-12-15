from django.contrib import admin
from .models import BlogPost, Category, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'post_count', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    
    def post_count(self, obj):
        return obj.blog_posts.count()
    post_count.short_description = 'Number of Posts'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'post_count', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    
    def post_count(self, obj):
        return obj.blog_posts.count()
    post_count.short_description = 'Number of Posts'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'published_date', 'view_count', 'is_featured')
    list_filter = ('status', 'category', 'author', 'is_featured', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('view_count', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'content', 'author', 'category')
        }),
        ('Tags and Status', {
            'fields': ('tags', 'status', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('published_date', 'created_at', 'updated_at', 'view_count')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)
