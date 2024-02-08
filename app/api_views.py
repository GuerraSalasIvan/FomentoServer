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
def ubicacion_list(request):
    ubicacion = (Ubicacion.objects.prefetch_related('equipo').prefetch_related('deporte')
               .all())
    serializer = UbicacionSerializer(ubicacion, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def liga_list(request):
    liga = (Liga.objects
               .all())
    serializer = LigaSerializer(liga, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def deporte_list(request):
    deporte = (Deportes.objects
               .all())
    serializer = DeporteSerializer(deporte, many=True)
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
    
# ------------------------- Busqueda avanzada equipo ---------------------------
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
    
    
# ------------------------- Busqueda avanzada ubicacion ---------------------------
@api_view(['GET'])
def ubicacion_busqueda_avanzada(request):

    if(len(request.query_params) > 0):
        formulario = BusquedaAvanzadaUbicacionForm(request.query_params)
        if formulario.is_valid():
        
            ubicacion = Ubicacion.objects.prefetch_related('deporte').prefetch_related('equipo')
            
            #Obtener filtros
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            capacidad = formulario.cleaned_data.get('capacidad')
            calle = formulario.cleaned_data.get('calle')
            
            if(textoBusqueda != ""):
                ubicacion = ubicacion.filter(Q(nombre__contains=textoBusqueda) | Q(deporte__deporte__contains=textoBusqueda))
                 
            if(capacidad != None):
                ubicacion = ubicacion.filter(capacidad__gt=capacidad)
                
            if(calle != None):
                ubicacion = ubicacion.filter(calle__contains=calle)
                
            ubicacion = ubicacion.all()
            
            serializer = UbicacionSerializer(ubicacion, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    
# ------------------------- Busqueda avanzada perfil publico ---------------------------
@api_view(['GET'])
def perfil_publico_busqueda_avanzada(request):

    if(len(request.query_params) > 0):
        formulario = BusquedaAvanzadaPerfil_PublicoForm(request.query_params)
        if formulario.is_valid():
        
            perfil_publico = Perfil_Publico.objects.select_related('lugar_fav')
            
            #Obtener filtros
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            #lugar_fav = formulario.cleaned_data.get('lugar_fav')
            
            if(textoBusqueda != ""):
                perfil_publico = perfil_publico.filter(descripcion__contains=textoBusqueda)
                
            '''
            if(len(lugar_fav) > 0):
                filtroOR = Q(lugar_fav = lugar_fav[0])
                for lugar_fav in lugar_fav[1:]:
                    filtroOR |= Q(lugar_fav=lugar_fav)
            '''
                
            perfil_publico = perfil_publico.all()
            
            serializer = Perfil_PublicoSerializer(perfil_publico, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET']) 
def obtener_equipo(request, equipo_id):
    equipo = Equipos.objects.select_related('deporte').prefetch_related('usuario')
    equipo = equipo.get(id=equipo_id)
    serializer = EquipoSerializer(equipo)
    return Response(serializer.data)

@api_view(['POST'])
def crear_equipo(request):
    serializers = EquipoSerializerCreate(data=request.data)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response('Equipo Creado')
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else: 
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    
@api_view(['PUT'])
def equipo_editar(request,equipo_id):
    pass
    
@api_view(['DELETE'])
def equipo_eliminar(request,equipo_id):
    equipo = Equipos.objects.get(id=equipo_id)
    try:
        equipo.delete()
        return Response("Equipo ELIMINADO")
    except Exception as error:
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
