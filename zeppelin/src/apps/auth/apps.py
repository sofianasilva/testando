from django.apps import AppConfig

class AuthConfig(AppConfig):
    name  = 'apps.auth'
    label = 'apps_auth'

    def ready(self):
        import apps.auth.signals
