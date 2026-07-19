from django.contrib import admin
from django.db import models
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline
from .models import AdminPage, PageBlock
from django_ckeditor_5.widgets import CKEditor5Widget


class DescriptionCKEditorMixin:
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')},
    }


class PageBlockInline(DescriptionCKEditorMixin, TranslationTabularInline):
    model = PageBlock
    extra = 1
    fields = ('order', 'block_type', 'title', 'description', 'date', 'photo', 'file', 'url', 'value', 'is_active')


@admin.register(AdminPage)
class AdminPageAdmin(DescriptionCKEditorMixin, TabbedTranslationAdmin):
    list_display = ('order', 'title', 'group', 'parent', 'is_development', 'is_active')
    list_filter = ('group', 'is_development', 'is_active')
    search_fields = ('title', 'description', 'slug')
    list_display_links = ('title',)
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('title_ru',)}
    inlines = [PageBlockInline]
    fieldsets = (
        ('Структура и навигация', {'fields': ('title', 'slug', 'group', 'parent', 'order', 'is_development', 'is_active')}),
        ('Контент страницы', {'fields': ('main_photo', 'description', 'redirect_url', 'pdf_file')}),
    )


@admin.register(PageBlock)
class PageBlockAdmin(DescriptionCKEditorMixin, TabbedTranslationAdmin):
    list_display = ('order', 'title', 'page', 'block_type', 'is_active')
    list_filter = ('page__group', 'page', 'block_type', 'is_active')
    search_fields = ('title', 'description', 'url', 'value')
    list_display_links = ('title',)
    list_editable = ('order',)
    fieldsets = (
        ('Основное', {'fields': ('page', 'order', 'block_type', 'title', 'description', 'is_active')}),
        ('Медиа, ссылки и значения', {'fields': ('date', 'photo', 'file', 'url', 'value')}),
    )
