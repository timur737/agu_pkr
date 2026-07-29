from modeltranslation.translator import TranslationOptions, register
from .models import AdminPage, News, PageBlock


@register(AdminPage)
class AdminPageTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(PageBlock)
class PageBlockTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'value')


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'detail_description')
