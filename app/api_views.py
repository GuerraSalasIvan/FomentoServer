from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .forms import *
from django.db.models import Q,Prefetch
from django.contrib.auth.models import Group
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics
from rest_framework.permissions import AllowAny
 

@api_view(['GET'])
def ubicacion_list(request):
    ubicacion = (Ubicacion.objects.prefetch_related('equipo').prefetch_related('deporte')
               .all())
    serializer = UbicacionSerializer(ubicacion, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def perfil_publico_list(request):
    perfil_publico = (Perfil_Publico.objects.select_related('lugar_fav')
               .all())
    serializer = Perfil_PublicoSerializer(perfil_publico, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def usuarios_list(request):
    usuarios = (Usuarios.objects.prefetch_related('rol')
               .all())
    serializer = UsuariosSerializer(usuarios, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def liga_list(request):
    liga = (Liga.objects
               .all())
    serializer = LigaSerializer(liga, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def colores_list(request):
    color = (Colores.objects
               .all())
    serializer = ColorSerializer(color, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def deporte_list(request):
    deporte = (Deportes.objects
               .all())
    serializer = DeporteSerializer(deporte, many=True)
    return Response(serializer.data)


################################## EQUIPO ######################################

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
    
    
@api_view(['GET']) 
def obtener_equipo(request, equipo_id):
    if(request.user.has_perm("equipo.view_equipos")):
    
        equipo = Equipos.objects.select_related('deporte').prefetch_related('usuario')
        equipo = equipo.get(id=equipo_id)
        serializer = EquipoSerializer(equipo)
        return Response(serializer.data)

@api_view(['POST'])
def crear_equipo(request):
    if(1):
        serializersEquipo = EquipoSerializerCreate(data=request.data)
        if serializersEquipo.is_valid():
            try:
                serializersEquipo.save()
                return Response('Equipo Creado')
            except Exception as error:
                return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else: 
            return Response(serializersEquipo.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    
@api_view(['PUT'])
def equipo_editar(request,equipo_id):
    if(request.user.has_perm("equipo.change_equipos")):
        equipo = Equipos.objects.get(id=equipo_id)
        serializers = EquipoSerializerCreate(data=request.data, instance=equipo)
        if serializers.is_valid():
            try:
                serializers.save()
                return Response('Equipo Editado')
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else: 
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST) 
    
@api_view(['PATCH'])
def equipo_actualizar_nombre(request,equipo_id):
    if(request.user.has_perm("equipo.change_equipos")):
        serializers = EquipoSerializerCreate(data=request.data)
        equipo = Equipos.objects.get(id=equipo_id)
        serializers = EquipoSerializerActualizarNombre(data=request.data,instance=equipo)
        if serializers.is_valid():
            try:
                serializers.save()
                return Response("Equipo EDITADO")
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def equipo_eliminar(request,equipo_id):
    if(request.user.has_perm("equipo.delete_equipos")):
        equipo = Equipos.objects.get(id=equipo_id)
        try:
            equipo.delete()
            return Response("Equipo ELIMINADO")
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
################################## UBICACION ######################################

 
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
    
@api_view(['GET']) 
def obtener_ubicacion(request, ubicacion_id):
    if(request.user.has_perm("ubicacion.view_ubicacion")):
    
        ubicacion = Ubicacion.objects.prefetch_related('deporte').prefetch_related('equipo')
        ubicacion = ubicacion.get(id=ubicacion_id)
        serializer = UbicacionSerializer(ubicacion)
        return Response(serializer.data)

@api_view(['POST'])
def crear_ubicacion(request):
    if(request.user.has_perm("ubicacion.add_ubicacion")):
    
        serializers = UbicacionSerializerCreate(data=request.data)
        if serializers.is_valid():
            try:
                serializers.save()
                return Response('Ubicacion Creada')
            except Exception as error:
                return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else: 
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def ubicacion_editar(request,ubicacion_id):
    if(request.user.has_perm("ubicacion.change_ubicacion")):
    
        ubicacion = Ubicacion.objects.get(id=ubicacion_id)
        serializers = UbicacionSerializerCreate(data=request.data, instance=ubicacion)
        if serializers.is_valid():
            try:
                serializers.save()
                return Response('ubicacion Editada')
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else: 
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def ubicacion_actualizar_nombre(request,ubicacion_id):
    if(request.user.has_perm("ubicacion.change_ubicacion")):
    
        serializers = UbicacionSerializerCreate(data=request.data)
        ubicacion = Ubicacion.objects.get(id=ubicacion_id)
        serializers = UbicacionSerializerActualizarNombre(data=request.data,instance=ubicacion)
        if serializers.is_valid():
            try:
                serializers.save()
                return Response("Ubicacion EDITADA")
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def ubicacion_eliminar(request,ubicacion_id):
    if(request.user.has_perm("ubicacion.delete_ubicacion")):
    
        ubicacion = Ubicacion.objects.get(id=ubicacion_id)
        try:
            ubicacion.delete()
            return Response('Ubicacion Creada')
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


############################### PERFIL PUBLICO ###################################
    
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
def obtener_perfil_publico(request, perfil_publico_id):
    if(request.user.has_perm("perfil_publico.view_perfil_publico")):
        perfil_publico = Perfil_Publico.objects.select_related('lugar_fav')
        perfil_publico = perfil_publico.get(id=perfil_publico_id)
        serializer = Perfil_PublicoSerializer(perfil_publico)
        return Response(serializer.data)


@api_view(['POST'])
def crear_perfil_publico(request):
    if(request.user.has_perm("perfil_publico.add_perfil_publico")):
    
        serializers = Perfil_PublicoSerializerCreate(data=request.data)
        if serializers.is_valid():
            try:
                serializers.save()
                return Response('Perfil publico Creado')
            except Exception as error:
                return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else: 
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def perfil_publico_editar(request,perfil_publico_id):
    if(request.user.has_perm("perfil_publico.change_perfil_publico")):
    
        perfil_publico = Perfil_Publico.objects.get(id=perfil_publico_id)
        serializers = Perfil_PublicoSerializerCreate(data=request.data, instance=perfil_publico)
        if serializers.is_valid():
            try:
                serializers.save()
                return Response('Perfil publico Editada')
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else: 
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def perfil_publico_eliminar(request,perfil_publico_id):
    if(request.user.has_perm("perfil_publico.delete_perfil_publico")):
    
        perfil_publico = Perfil_Publico.objects.get(id=perfil_publico_id)
        try:
            perfil_publico.delete()
            return Response('Perfil publico Creado')
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    perfil_publico = Perfil_Publico.objects.get(id=perfil_publico_id)
    try:
        perfil_publico.delete()
        return Response('Perfil publico Creado')
    except Exception as error:
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
################################# PARTIDOS #####################################

@api_view(['GET'])
def partido_list(request):
    partido = (Partido.objects
               .select_related('equipo_local')
               .select_related('equipo_visitante')
               .select_related('ubicacion')
               .all())
    serializer = PartidoSerializer(partido, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def crear_partido(request):
    serializers = PartidoSerializerCreate(data=request.data)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response('Partido Creado')
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else: 
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


############################### REGISTRATION ###################################


class registrar_usuario(generics.CreateAPIView):
    
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        print(request.body)
        serializer = UsuarioSerializerRegistro(data=request.data)
        if serializer.is_valid():
            try:
                rol = int(request.data.get('rol'))
                user = UserLogin.objects.create_user(
                    username = serializer.data.get("username"),
                    email = serializer.data.get("email"),
                    password = serializer.data.get("password1"),
                    rol = rol,   
                )
                
                if(rol == UserLogin.cliente):
                    print(Group.objects.all())
                    grupo = Group.objects.get(name='cliente') 
                    grupo.user_set.add(user)
                    cliente = Usuarios.objects.create( 
                                                      rol = user,
                                                      edad = serializer.data.get("edad"),
                                                      sexo = serializer.data.get("sexo"),
                                                      )
                    cliente.save()
                elif(rol == UserLogin.entrenador):
                    grupo = Group.objects.get(name='entrenador') 
                    grupo.user_set.add(user)
                    entrenador = Entrenador.objects.create(
                                                            rol = user,
                                                            edad = serializer.data.get("edad"),
                                                            sexo = serializer.data.get("sexo"),
                                                          )
                    entrenador.save()
                usuarioSerializado = UserLoginSerializer(user)
                return Response(usuarioSerializado.data)
            
            except Exception as error:
                print(repr(error))
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  


from oauth2_provider.models import AccessToken    
@api_view(['GET'])
def obtener_usuario_token(request,token):
    ModeloToken = AccessToken.objects.get(token=token)
    usuario = UserLogin.objects.get(id=ModeloToken.id)
    serializer = UserLoginSerializer(usuario)
    return Response(serializer.data)
    
