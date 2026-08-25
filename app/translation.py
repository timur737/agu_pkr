from modeltranslation.translator import TranslationOptions, register
from .models import AdminPage, News, PageBlock


@register(AdminPage)
class AdminPageTranslationOptions(TranslationOptions):
    fields = ('title', 'content_title', 'description')


@register(PageBlock)
class PageBlockTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'short_information', 'contacts', 'value')


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'detail_description')
