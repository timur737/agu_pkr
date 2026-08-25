from django import forms
from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline
from .models import AdminPage, News, NewsPhoto, PageBlock
from django.utils.html import format_html
from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline
from .widgets import CKEditorTextarea


class DescriptionCKEditorMixin:
    formfield_overrides = {
        models.TextField: {'widget': CKEditorTextarea},
    }


class NewsAdminForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('show_on_home'):
            return cleaned

        position = cleaned.get('home_order')
        if position not in (1, 2, 3):
            self.add_error('home_order', 'Для главной страницы выберите позицию 1, 2 или 3.')
            return cleaned

        occupied = News.objects.filter(show_on_home=True, home_order=position)
        if self.instance.pk:
            occupied = occupied.exclude(pk=self.instance.pk)
        if occupied.exists():
            self.add_error('home_order', f'Позиция {position} на главной странице уже занята.')
        return cleaned


class PageBlockInline(DescriptionCKEditorMixin, TranslationStackedInline):
    model = PageBlock
    # Empty inline forms used to be submitted as a block with order=0.  Blocks
    # must only be created after the editor explicitly presses "Add another".
    extra = 0
    fields = (
        'order', 'block_type', 'title', 'description', 'short_information',
        'contacts', 'email', 'date', 'photo', 'file', 'url', 'value', 'is_active',
    )

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
        ('Контент страницы', {'fields': ('content_title', 'main_photo', 'description', 'redirect_url', 'pdf_file')}),
    )

    @admin.display(description='Страница', ordering='order')
    def structured_title(self, obj):
        """Make the page/subpage relationship visible in the page list."""
        prefix = '↳ ' if obj.parent_id else ''
        return format_html('<span class="admin-page-depth-{}">{}{}</span>', 1 if obj.parent_id else 0, prefix, obj.title)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent')

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))
        if obj and obj.group == AdminPage.GROUP_HOME and not obj.parent_id:
            fieldsets.append(('1.5. Новости', {'fields': ('news_management',)}))
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if obj and obj.group == AdminPage.GROUP_HOME and not obj.parent_id:
            fields.append('news_management')
        return fields

    @admin.display(description='Подразделы новостей')
    def news_management(self, obj):
        changelist = reverse('admin:app_news_changelist')
        add_url = reverse('admin:app_news_add')
        return format_html(
            '<a class="button" href="{}?show_on_home__exact=1">1.5.1. Новости на главной</a> '
            '<a class="button" href="{}">1.5.2. Общая страница новостей</a> '
            '<a class="button" href="{}">Добавить новость</a>',
            changelist, changelist, add_url,
        )


@admin.register(News)
class NewsAdmin(DescriptionCKEditorMixin, TabbedTranslationAdmin):
    form = NewsAdminForm
    list_display = ('order', 'title', 'published_at', 'show_on_home', 'home_order', 'is_active')
    list_filter = ('show_on_home', 'is_active', 'published_at')
    search_fields = ('title', 'description', 'detail_description', 'slug')
    list_display_links = ('title',)
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('title_ru',)}
    fieldsets = (
        ('1.5.1. Новости на главной — не более 3', {
            'fields': ('show_on_home', 'home_order'),
            'description': 'Отметьте новость для главной страницы и задайте позицию от 1 до 3.',
        }),
        ('1.5.2. Новости — общая страница', {
            'fields': ('title', 'slug', 'photo', 'description', 'published_at', 'order', 'is_active'),
        }),
        ('1.5.3. Страница выбранной новости', {
            'fields': ('detail_description',),
            'description': 'Фотографии страницы добавляются отдельными блоками ниже.',
        }),
    )

    class NewsPhotoInline(admin.TabularInline):
        model = NewsPhoto
        extra = 0
        fields = ('order', 'photo')

    inlines = (NewsPhotoInline,)
