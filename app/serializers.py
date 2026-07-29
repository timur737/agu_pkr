from rest_framework import serializers
from .models import AdminPage, News, PageBlock


class PageBlockSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = PageBlock
        fields = [
            'id', 'block_type', 'title', 'description', 'date', 'photo', 'photo_url',
            'file', 'file_url', 'url', 'value', 'order', 'created_at', 'updated_at'
        ]

    def _absolute_url(self, file_field):
        if not file_field:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(file_field.url)
        return file_field.url

    def get_photo_url(self, obj):
        return self._absolute_url(obj.photo)

    def get_file_url(self, obj):
        return self._absolute_url(obj.file)


class AdminPageListSerializer(serializers.ModelSerializer):
    main_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = AdminPage
        fields = [
            'id', 'title', 'slug', 'group', 'parent', 'order', 'main_photo',
            'main_photo_url', 'description', 'redirect_url', 'pdf_file',
            'is_development', 'created_at', 'updated_at'
        ]

    def get_main_photo_url(self, obj):
        if not obj.main_photo:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.main_photo.url)
        return obj.main_photo.url


class AdminPageSerializer(AdminPageListSerializer):
    blocks = PageBlockSerializer(many=True, read_only=True)
    subpages = serializers.SerializerMethodField()
    pdf_file_url = serializers.SerializerMethodField()

    class Meta(AdminPageListSerializer.Meta):
        fields = AdminPageListSerializer.Meta.fields + ['pdf_file_url', 'blocks', 'subpages']

    def get_pdf_file_url(self, obj):
        if not obj.pdf_file:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.pdf_file.url)
        return obj.pdf_file.url

    def get_subpages(self, obj):
        subpages = obj.subpages.filter(is_active=True).prefetch_related('blocks')
        return AdminPageSerializer(subpages, many=True, context=self.context).data


class NewsListSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'photo', 'photo_url', 'description',
            'published_at', 'order', 'created_at', 'updated_at',
        ]

    def _absolute_url(self, image):
        if not image:
            return None
        request = self.context.get('request')
        return request.build_absolute_uri(image.url) if request else image.url

    def get_photo_url(self, obj):
        return self._absolute_url(obj.photo)


class NewsSerializer(NewsListSerializer):
    detail_photo_1_url = serializers.SerializerMethodField()
    detail_photo_2_url = serializers.SerializerMethodField()
    detail_photo_3_url = serializers.SerializerMethodField()

    class Meta(NewsListSerializer.Meta):
        fields = NewsListSerializer.Meta.fields + [
            'detail_description',
            'detail_photo_1', 'detail_photo_1_url',
            'detail_photo_2', 'detail_photo_2_url',
            'detail_photo_3', 'detail_photo_3_url',
        ]

    def get_detail_photo_1_url(self, obj):
        return self._absolute_url(obj.detail_photo_1)

    def get_detail_photo_2_url(self, obj):
        return self._absolute_url(obj.detail_photo_2)

    def get_detail_photo_3_url(self, obj):
        return self._absolute_url(obj.detail_photo_3)
