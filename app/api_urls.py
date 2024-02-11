from django.urls import path
from .api_views import *

urlpatterns= [
    #-------------------- EQUIPOS -------------------
    path('equipos',equipo_list),
    path('equipos/<int:equipo_id>', obtener_equipo),
    path('busqueda/equipo_simple', equipo_buscar),
    path('equipos/busqueda_avanzada', equipos_busqueda_avanzada),
    path('equipos/editar/<int:equipo_id>', equipo_editar),
    path('equipos/crear', crear_equipo),
    path('equipos/eliminar/<int:equipo_id>',equipo_eliminar),
    
    #------------------- UBICACION ------------------
    path('ubicacion', ubicacion_list),
    path('ubicacion/<int:ubicacion_id>', obtener_ubicacion),
    path('ubicacion/busqueda_avanzada', ubicacion_busqueda_avanzada),
    path('ubicacion/crear', crear_ubicacion),
    path('ubicacion/editar/<int:ubicacion_id>', ubicacion_editar),
    path('ubicacion/eliminar/<int:ubicacion_id>',ubicacion_eliminar),
    
    #-------------------- DEPORTE -------------------
    path('deporte', deporte_list),
    
    #--------------------- LIGA ---------------------
    path('ligas', liga_list),
    
    #----------------- PERFIL PUBLICO ---------------
    path('perfil_publico/busqueda_avanzada', perfil_publico_busqueda_avanzada),
    path('perfil_publico/<int:perfil_publico_id>', obtener_perfil_publico),
    path('perfil_publico/crear', crear_perfil_publico),
    path('perfil_publico/editar/<int:perfil_publico_id>', perfil_publico_editar),
    path('perfil_publico/eliminar/<int:perfil_publico_id>',perfil_publico_eliminar),
    
    
    
    
]