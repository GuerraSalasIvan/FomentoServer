from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .forms import *
from django.db.models import Q,Prefetch

@api_view(['GET'])
def equipo_list(request):
    equipos = (Equipos.objects.select_related("deporte","liga")
               .all())
    serializer = EquipoSerializer(equipos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def equipo_buscar(request):
    
    formulario = BusquedaEquipoForm(request.query_params)
    if(formulario.is_valid()):
        texto = formulario.data.get('textoBusqueda')
        equipos = Equipos.objects.select_related('deporte').prefetch_related('usuario')
        equipos = equipos.filter(nombre__contains=texto).all()
        serializer = EquipoSerializer(equipos, many=True)
        return Response(serializer.data)
    else:
        return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)