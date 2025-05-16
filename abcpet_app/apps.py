from django.apps import AppConfig

class AbcpetAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'abcpet_app'

    def ready(self):
        import abcpet_app.signals