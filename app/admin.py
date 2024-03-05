from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Usuarios)
admin.site.register(Equipos)
admin.site.register(Deportes)
admin.site.register(Votacion)
admin.site.register(UserLogin)
admin.site.register(Perfil_Publico)
admin.site.register(Detalles_Ubicacion)
admin.site.register(Liga)
admin.site.register(Ubicacion)
admin.site.register(Rel_Usu_Equi)
admin.site.register(Partido)
admin.site.register(Colores)

