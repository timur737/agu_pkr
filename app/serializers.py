from rest_framework import serializers
from .models import AdminPage, News, NewsPhoto, PageBlock


class PageBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageBlock
        fields = [
            'id', 'page', 'block_type', 'title', 'description', 'short_information',
            'contacts', 'email', 'date', 'image_ru', 'image_ky', 'image_en',
            'file_ru', 'file_ky', 'file_en',
            'url', 'value', 'order', 'created_at', 'updated_at'
        ]

    def _absolute_url(self, file_field):
        if not file_field:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(file_field.url)
        return file_field.url

class AdminPageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminPage
        fields = [
            'id', 'title', 'slug', 'group', 'parent', 'order', 'image_ru', 'image_ky', 'image_en',
            'content_title', 'description', 'redirect_url', 'file_ru', 'file_ky', 'file_en',
            'is_development', 'created_at', 'updated_at'
        ]


class AdminPageSerializer(AdminPageListSerializer):
    blocks = PageBlockSerializer(many=True, read_only=True)
    subpages = serializers.SerializerMethodField()

    class Meta(AdminPageListSerializer.Meta):
        fields = AdminPageListSerializer.Meta.fields + ['blocks', 'subpages']

    def get_subpages(self, obj):
        subpages = obj.subpages.filter(is_active=True).prefetch_related('blocks')
        return AdminPageSerializer(subpages, many=True, context=self.context).data


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'image_ru', 'image_ky', 'image_en', 'description',
            'published_at', 'order', 'show_on_home', 'home_order',
            'created_at', 'updated_at',
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        show_on_home = attrs.get('show_on_home', getattr(self.instance, 'show_on_home', False))
        home_order = attrs.get('home_order', getattr(self.instance, 'home_order', 0))
        if show_on_home and home_order not in (1, 2, 3):
            raise serializers.ValidationError({'home_order': 'Выберите позицию 1, 2 или 3.'})
        if show_on_home:
            occupied = News.objects.filter(show_on_home=True, home_order=home_order)
            if self.instance:
                occupied = occupied.exclude(pk=self.instance.pk)
            if occupied.exists():
                raise serializers.ValidationError({'home_order': 'Эта позиция на главной уже занята.'})
        return attrs

class NewsPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsPhoto
        fields = ['id', 'image_ru', 'image_ky', 'image_en', 'order']


class NewsSerializer(NewsListSerializer):
    detail_photos = NewsPhotoSerializer(many=True, read_only=True)

    class Meta(NewsListSerializer.Meta):
        fields = NewsListSerializer.Meta.fields + [
            'detail_description',
            'detail_photos',
        ]

