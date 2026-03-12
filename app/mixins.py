from django.utils import translation


class LanguageMixin:
    """
    Mixin для поддержки многоязычности в API
    Поддерживает язык через параметр ?lang= или заголовок Accept-Language
    """
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        
        # Получаем язык из параметра запроса или заголовка
        lang = request.query_params.get('lang') or request.META.get('HTTP_ACCEPT_LANGUAGE', '').split(',')[0].split('-')[0]
        
        # Проверяем, что язык поддерживается
        supported_languages = ['ru', 'ky', 'en']
        if lang not in supported_languages:
            lang = 'ru'  # Язык по умолчанию
        
        # Активируем язык
        translation.activate(lang)
        request.LANGUAGE_CODE = lang
    
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        # Деактивируем язык после ответа
        translation.deactivate()
        return response

