from django.utils.translation import activate
from django.conf import settings

class IdiomaDinamicoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Un ejemplo: si pasas el idioma por parámetro en la URL (?lang=fi) 
        # o si lo detectas desde la sesión/cookie
        idioma = request.GET.get('lang') or request.session.get('django_language')
        
        # Si el idioma está permitido en tu lista de settings.py, lo activamos
        if idioma in [lang[0] for lang in settings.LANGUAGES]:
            activate(idioma)
            request.LANGUAGE_CODE = idioma
        else:
            # Si no hay parámetro, que use el idioma por defecto ('es')
            activate(settings.LANGUAGE_CODE)
            
        response = self.get_response(request)
        return response