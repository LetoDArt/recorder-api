from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/stream/(?P<username>[^/]+)/$', consumers.StreamerConsumer.as_asgi())
]
