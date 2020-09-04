from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chatapp.routing
import account.routing
from django.urls import path, re_path

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/chat/(?P<room_name>\w+)/$', chatapp.consumers.ChatConsumer),
            path('ws/notifications/', account.consumers.NotificationsConsumer),
        ])
    ),
})