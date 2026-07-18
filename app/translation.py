from modeltranslation.translator import TranslationOptions, register
from .models import AdminPage, PageBlock


@register(AdminPage)
class AdminPageTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(PageBlock)
class PageBlockTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'value')
