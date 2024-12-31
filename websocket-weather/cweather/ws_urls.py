import djstorm.ws
from django.urls import path

urlpatterns = [
    path("ws", djstorm.ws.WeatherSocket),
    path("ws2", djstorm.ws.WeatherSocket2),
]
