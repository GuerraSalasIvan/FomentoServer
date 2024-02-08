from django.urls import path
from .api_views import *

urlpatterns= [
    path('equipos',equipo_list),
    path('equipos/<int:equipo_id>', obtener_equipo),
    path('equipos/editar/<int:equipo_id>', equipo_editar),
    path('ligas', liga_list),
    path('deporte', deporte_list),
    path('ubicacion', ubicacion_list),
    path('ubicacion/<int:ubicacion_id>', obtener_ubicacion),
    
    path('busqueda/equipo_simple', equipo_buscar),
    path('equipos/busqueda_avanzada', equipos_busqueda_avanzada),
    
    path('ubicacion/busqueda_avanzada', ubicacion_busqueda_avanzada),
    
    path('perfil_publico/busqueda_avanzada', perfil_publico_busqueda_avanzada),
    path('perfil_publico/<int:perfil_publico_id>', obtener_perfil_publico),
    
    path('equipos/crear', crear_equipo),
    
    path('equipos/eliminar/<int:equipo_id>',equipo_eliminar),
]