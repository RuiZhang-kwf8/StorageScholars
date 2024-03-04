from django.urls import re_path
from store.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<random_string>\w+)/$', ChatConsumer.as_asgi()),
]
