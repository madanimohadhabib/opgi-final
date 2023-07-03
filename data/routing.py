from django.urls import re_path 
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/socket-server/', consumers.ChatConsumer.as_asgi())
]

class SecondDBRouter:
    """
    A router to control all database operations on models in the
    secondapp application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'secondapp':
            return 'second_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'secondapp':
            return 'second_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'secondapp' or obj2._meta.app_label == 'secondapp':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'second_db':
            return app_label == 'secondapp'
        elif app_label == 'secondapp':
            return False
        return None
