from rest_framework import viewsets, filters
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from .mixins import LanguageMixin
from .models import AdminPage, News, PageBlock
from .serializers import (
    AdminPageSerializer, AdminPageListSerializer, NewsListSerializer,
    NewsSerializer, PageBlockSerializer,
)


class PageBlockFilter(django_filters.FilterSet):
    page_id = django_filters.NumberFilter(field_name='page_id')

    class Meta:
        model = PageBlock
        fields = ['page_id', 'block_type']


class AdminPageViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = AdminPage.objects.filter(is_active=True).prefetch_related('blocks', 'subpages__blocks')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['group', 'parent', 'is_development']
    search_fields = ['title', 'description', 'slug']
    ordering_fields = ['order', 'created_at']
    ordering = ['order', 'id']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return AdminPageListSerializer
        return AdminPageSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class PageBlockViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = PageBlock.objects.filter(is_active=True).select_related('page')
    serializer_class = PageBlockSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PageBlockFilter
    search_fields = ['title', 'description', 'url', 'value']
    ordering_fields = ['order', 'created_at']
    ordering = ['page__order', 'order', 'id']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class NewsViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = News.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'detail_description']
    ordering_fields = ['order', 'published_at', 'created_at']
    ordering = ['order', '-published_at', '-id']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return NewsListSerializer
        return NewsSerializer
