from rest_framework import viewsets, generics, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import BlogPost, Category, Tag
from .serializers import (
    BlogPostListSerializer, BlogPostDetailSerializer,
    CategorySerializer, TagSerializer
)
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly, IsAuthorOrAdmin
from .filters import BlogPostFilter
from django.utils import timezone

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.annotate(post_count=Count('blog_posts'))
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def posts(self, request, pk=None):
        category = self.get_object()
        posts = category.blog_posts.filter(status='published')
        serializer = BlogPostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.annotate(post_count=Count('blog_posts'))
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def posts(self, request, pk=None):
        tag = self.get_object()
        posts = tag.blog_posts.filter(status='published')
        serializer = BlogPostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

class BlogPostViewSet(viewsets.ModelViewSet):
    serializer_class = BlogPostDetailSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BlogPostFilter
    search_fields = ['title', 'content', 'author__username', 'category__name', 'tags__name']
    ordering_fields = ['published_date', 'created_at', 'view_count', 'title']
    ordering = ['-published_date']
    
    def get_queryset(self):
        queryset = BlogPost.objects.select_related('author', 'category').prefetch_related('tags')
        
        # Filter based on user permissions
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                # Admins can see all posts
                return queryset
            # Authenticated users can see their own drafts and all published posts
            return queryset.filter(
                Q(status='published') | Q(author=self.request.user)
            )
        else:
            # Anonymous users can only see published posts
            return queryset.filter(status='published')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPostListSerializer
        return BlogPostDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        post = self.get_object()
        if post.author != request.user and not request.user.is_staff:
            return Response(
                {"error": "You don't have permission to publish this post"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        post.status = 'published'
        if not post.published_date:
            post.published_date = timezone.now()
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        post = self.get_object()
        post.view_count += 1
        post.save()
        return Response({'view_count': post.view_count})
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def by_author(self, request):
        author_id = request.query_params.get('author')
        if not author_id:
            return Response(
                {"error": "Author ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        posts = BlogPost.objects.filter(
            author_id=author_id,
            status='published'
        )
        serializer = BlogPostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def by_category(self, request):
        category_id = request.query_params.get('category')
        if not category_id:
            return Response(
                {"error": "Category ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        posts = BlogPost.objects.filter(
            category_id=category_id,
            status='published'
        )
        serializer = BlogPostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def featured(self, request):
        posts = BlogPost.objects.filter(
            is_featured=True,
            status='published'
        ).order_by('-published_date')
        serializer = BlogPostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def recent(self, request):
        posts = BlogPost.objects.filter(
            status='published'
        ).order_by('-published_date')[:10]
        serializer = BlogPostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_posts(self, request):
        posts = BlogPost.objects.filter(author=request.user)
        serializer = BlogPostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)