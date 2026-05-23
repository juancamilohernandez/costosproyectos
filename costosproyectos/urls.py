from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

# Rutas globales neutrales
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# Rutas que llevan prefijo de idioma (/es/, /da/)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('costos_app.urls')),
    prefix_default_language=True,
)