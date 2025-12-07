from rest_framework import serializers
from .models import BlogPost, Category, Tag
from accounts.serializers import UserBriefSerializer

class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'created_at', 'post_count')

class TagSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Tag
        fields = ('id', 'name', 'created_at', 'post_count')

class BlogPostListSerializer(serializers.ModelSerializer):
    author = UserBriefSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    excerpt = serializers.SerializerMethodField()
    read_time = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = (
            'id', 'title', 'excerpt', 'author', 'category',
            'tags', 'published_date', 'status', 'view_count',
            'is_featured', 'read_time', 'created_at'
        )
        read_only_fields = ('published_date', 'view_count')
    
    def get_excerpt(self, obj):
        return obj.excerpt
    
    def get_read_time(self, obj):
        return obj.read_time

class BlogPostDetailSerializer(serializers.ModelSerializer):
    author = UserBriefSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False
    )
    
    class Meta:
        model = BlogPost
        fields = '__all__'
        read_only_fields = (
            'author', 'view_count', 'created_at', 'updated_at'
        )
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['tags'] = TagSerializer(instance.tags.all(), many=True).data
        return representation