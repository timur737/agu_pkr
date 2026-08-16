from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline
from .models import AdminPage, News, PageBlock
from .widgets import CKEditorTextarea


class DescriptionCKEditorMixin:
    formfield_overrides = {
        models.TextField: {'widget': CKEditorTextarea},
    }


class PageBlockInline(DescriptionCKEditorMixin, TranslationStackedInline):
    model = PageBlock
    # Empty inline forms used to be submitted as a block with order=0.  Blocks
    # must only be created after the editor explicitly presses "Add another".
    extra = 0
    fields = ('order', 'block_type', 'title', 'description', 'date', 'photo', 'file', 'url', 'value', 'is_active')

    class Media:
        css = {'all': ('app/admin/content_structure.css',)}
        js = ('app/admin/page_blocks.js',)


@admin.register(AdminPage)
class AdminPageAdmin(DescriptionCKEditorMixin, TabbedTranslationAdmin):
    list_display = ('order', 'structured_title', 'group', 'parent', 'is_development', 'is_active')
    list_filter = ('group', 'is_development', 'is_active')
    search_fields = ('title', 'description', 'slug')
    list_display_links = ('structured_title',)
    list_editable = ('order',)
    ordering = ('order', 'id')
    prepopulated_fields = {'slug': ('title_ru',)}
    inlines = [PageBlockInline]
    fieldsets = (
        ('Структура и навигация', {'fields': ('title', 'slug', 'group', 'parent', 'order', 'is_development', 'is_active')}),
        ('Контент страницы', {'fields': ('main_photo', 'description', 'redirect_url', 'pdf_file')}),
    )

    @admin.display(description='Страница', ordering='order')
    def structured_title(self, obj):
        """Make the page/subpage relationship visible in the page list."""
        prefix = '↳ ' if obj.parent_id else ''
        return format_html('<span class="admin-page-depth-{}">{}{}</span>', 1 if obj.parent_id else 0, prefix, obj.title)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent')


@admin.register(News)
class NewsAdmin(DescriptionCKEditorMixin, TabbedTranslationAdmin):
    list_display = ('order', 'title', 'published_at', 'is_active')
    list_filter = ('is_active', 'published_at')
    search_fields = ('title', 'description', 'detail_description', 'slug')
    list_display_links = ('title',)
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('title_ru',)}
    fieldsets = (
        ('Карточка в списке новостей', {
            'fields': ('title', 'slug', 'photo', 'description', 'published_at', 'order', 'is_active'),
        }),
        ('Страница выбранной новости', {
            'fields': ('detail_description', 'detail_photo_1', 'detail_photo_2', 'detail_photo_3'),
            'description': 'Эти поля отображаются после перехода на выбранную новость.',
        }),
    )
