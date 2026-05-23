from django.apps import AppConfig


class CostosAppConfig(AppConfig):
    name = 'costos_app'


class CostosAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'costos_app'

    def ready(self):
        import costos_app.signals  # <-- Con esto se activan los correos automáticos
