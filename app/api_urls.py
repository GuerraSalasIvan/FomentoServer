from django.urls import path
from .api_views import *

urlpatterns= [
    path('equipos',equipo_list),
]