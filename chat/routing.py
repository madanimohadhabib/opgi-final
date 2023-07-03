from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    # Add more WebSocket URL patterns here
    re_path(r"ws/test/$",consumers.MyConsumer.as_asgi()),

]