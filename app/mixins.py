from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils import translation


DEFAULT_LANGUAGE = getattr(settings, 'MODELTRANSLATION_DEFAULT_LANGUAGE', settings.LANGUAGE_CODE)
SUPPORTED_LANGUAGES = {
    code.split('-')[0]
    for code, _ in getattr(settings, 'LANGUAGES', ((DEFAULT_LANGUAGE, ''),))
}


class LanguageMixin:
    """
    Mixin для поддержки многоязычности в API
    Поддерживает язык через заголовки Language, X-Language или Accept-Language.
    """
    language_headers = ('Language', 'X-Language', 'Accept-Language')

    def get_language_from_headers(self, request):
        for header in self.language_headers:
            value = request.headers.get(header)
            if not value:
                continue

            for part in value.split(','):
                lang = part.split(';')[0].strip().split('-')[0].lower()
                if lang in SUPPORTED_LANGUAGES:
                    return lang

        return DEFAULT_LANGUAGE

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        lang = self.get_language_from_headers(request)
        translation.activate(lang)
        request.LANGUAGE_CODE = lang
    
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        response['Content-Language'] = getattr(request, 'LANGUAGE_CODE', DEFAULT_LANGUAGE)
        patch_vary_headers(response, self.language_headers)
        translation.deactivate()
        return response
