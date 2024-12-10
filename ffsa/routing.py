from django.urls import path
from ffsa import consumers

websocket_urlpatterns = [
    path('ws/match/<str:match_id>/', consumers.MatchConsumer.as_asgi()),
]
