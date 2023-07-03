from channels.routing import ProtocolTypeRouter, URLRouter
import os
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opgi.settings')

asgi_application = get_asgi_application() #new

import recouvrement.routing #new
import chat.routing #new

application = ProtocolTypeRouter({
            "http": asgi_application,
            "websocket": URLRouter(recouvrement.routing.websocket_urlpatterns +
        chat.routing.websocket_urlpatterns) 
                       })
