from django.apps import AppConfig


class ManagerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manager_app'

    def ready(self):
        import manager_app.signals