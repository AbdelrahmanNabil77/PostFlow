import django_filters
from .models import BlogPost
from django.db.models import Q

class BlogPostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    content = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    tags = django_filters.CharFilter(method='filter_tags')
    published_after = django_filters.DateFilter(field_name='published_date', lookup_expr='gte')
    published_before = django_filters.DateFilter(field_name='published_date', lookup_expr='lte')
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = BlogPost
        fields = ['status', 'category', 'author', 'is_featured']
    
    def filter_tags(self, queryset, name, value):
        tag_names = value.split(',')
        return queryset.filter(tags__name__in=tag_names).distinct()
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(content__icontains=value) |
            Q(author__username__icontains=value) |
            Q(category__name__icontains=value) |
            Q(tags__name__icontains=value)
        ).distinct()