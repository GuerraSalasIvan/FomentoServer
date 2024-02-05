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
    

@api_view(['GET'])
def equipos_busqueda_avanzada(request):

    if(len(request.query_params) > 0):
        formulario = BusquedaAvanzadaEquipoForm(request.query_params)
        if formulario.is_valid():
        
            equipos = Equipos.objects.select_related('deporte').prefetch_related('usuario')
            
            #Obtener filtros
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            capacidad = formulario.cleaned_data.get('capacidad')
            
            if(textoBusqueda != ""):
                equipos = equipos.filter(Q(nombre__contains=textoBusqueda) | Q(deporte__deporte__contains=textoBusqueda))
                 
            if(capacidad != None):
                equipos = equipos.filter(capacidad__gt=capacidad)
                
            equipo = equipos.all()
            
            serializer = EquipoSerializer(equipo, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)