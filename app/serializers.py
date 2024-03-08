from rest_framework import serializers
from .models import *
import datetime


################################## USUARIOS ######################################

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta():
        model = UserLogin
        fields = '__all__'
        
class UsuariosSerializer(serializers.ModelSerializer):
    
    rol = UserLoginSerializer()
    
    class Meta():
        model = Usuarios
        fields = '__all__'

class UsuarioSerializerRegistro(serializers.Serializer):
 
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField()
    rol = serializers.IntegerField()
    
    def validate_username(self,username):
        usuario = UserLogin.objects.filter(username=username).first()
        if(not usuario is None):
            raise serializers.ValidationError('Ya existe un usuario con ese nombre')
        return username
    
#################################### LIGA ######################################

class LigaSerializer(serializers.ModelSerializer):
    class Meta():
        model = Liga
        fields = ['id','liga']
        
################################### COLOR ######################################

class ColorSerializer(serializers.ModelSerializer):
    class Meta():
        model = Colores
        fields = ['id','color']

################################## DEPORTE ######################################

class DeporteSerializer(serializers.ModelSerializer):
        
    class Meta():
        model = Deportes
        fields = '__all__'
        
################################## PERFIL PUBLICO ######################################

class Perfil_PublicoSerializer(serializers.ModelSerializer):
        
    class Meta():
        model = Perfil_Publico
        fields = ['id','descripcion','deportes_fav','hitos_publicos','lugar_fav', 'usuarios']

class Perfil_PublicoSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Perfil_Publico
        fields = ['id','descripcion','deportes_fav','hitos_publicos','lugar_fav', 'usuarios']
        '''
        def validate_descripcion(self,descripcion):
        perfil_publicoDescripcion = Perfil_Publico.objects.filter(descripcion=descripcion).first()
        
        if(not perfil_publicoDescripcion is None):
            if(not self.instance is None and perfil_publicoDescripcion.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('Ya existe un equipo con ese nombre')
        return descripcion
        '''

'''
NO LE VEO SENTIDO UN PATCH PARA PERFIL PUBLICO
'''
    
        
        
################################## EQUIPO ######################################
       
class EquipoSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Equipos
        fields=['nombre','deporte','media_equipo','color_eq_1','color_eq_2','liga','capacidad','usuario']
        
    def validate_nombre(self,nombre):
        equipoNombre = Equipos.objects.filter(nombre=nombre).first()
        
        if(not equipoNombre is None):
            if(not self.instance is None and equipoNombre.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('Ya existe un equipo con ese nombre')
        return nombre
    
    def validate_capacidad(self,capacidad):
        if (not (capacidad <= len(self.initial_data['usuario']))):
            pass
        else:
            raise serializers.ValidationError('No puede haber mas de'+ capacidad 
                                              +'miembros en este equipo')
        return capacidad
    
    def create(self, validated_data):
        n_miebros = len(self.initial_data['usuario'])
        lista_usu = []
        for usuario in self.initial_data['usuario']:
            modeloUsuario = Usuarios.objects.get(id=usuario)
            lista_usu.append(modeloUsuario.media)
            
        puntos_totales = sum(lista_usu)
        print(n_miebros)
        print(puntos_totales)
        
        media_equip = puntos_totales/n_miebros
        
        equipo = Equipos.objects.create(
            nombre = validated_data['nombre'],
            media_equipo = media_equip,
            color_eq_1 = validated_data['color_eq_1'],
            color_eq_2 = validated_data['color_eq_2'],
            liga = validated_data['liga'],
            deporte = validated_data['deporte'],
            capacidad = validated_data['capacidad'],     
        )
        
        for usuario in self.initial_data['usuario']:
            modeloUsuario = Usuarios.objects.get(id=usuario)
            Rel_Usu_Equi.objects.create(usuario=modeloUsuario, equipos=equipo)
        
        return equipo
       

class EquipoSerializer(serializers.ModelSerializer):
    
    usuario = UsuariosSerializer(many=True)
    liga = LigaSerializer()
    deporte = DeporteSerializer()
    
    class Meta:
        model = Equipos
        fields = ['id','nombre','media_equipo','color_eq_1','color_eq_2','deporte','liga','capacidad','usuario']

class EquipoSerializerActualizarNombre(serializers.ModelSerializer):
 
    class Meta:
        model = Equipos
        fields = ['nombre']
    
    def validate_nombre(self,nombre):
        equipoNombre = Equipos.objects.filter(nombre=nombre).first()
        if(not equipoNombre is None and equipoNombre.id != self.instance.id):
            raise serializers.ValidationError('Ya existe un equipo con ese nombre')
        return nombre
        
################################## UBICACION ######################################

class UbicacionSerializer(serializers.ModelSerializer):
        
    class Meta():
        model = Ubicacion
        fields = ['id','nombre','capacidad','calle','equipo','deporte']
        
        
class UbicacionSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Ubicacion
        fields = ['id','nombre','capacidad','calle','deporte']
        
    def validate_nombre(self,nombre):
        ubicacionNombre = Ubicacion.objects.filter(nombre=nombre).first()
        
        if(not ubicacionNombre is None):
            if(not self.instance is None and ubicacionNombre.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('Ya existe una ubicacion con ese nombre')
        return nombre
    
    def validate_calle(self,calle):
        ubicacionCalle = Ubicacion.objects.filter(calle=calle).first()
        
        if(not ubicacionCalle is None):
            if(not self.instance is None and ubicacionCalle.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('Ya existe un ubicacion en esta calle')
        return calle
    
class UbicacionSerializerActualizarNombre(serializers.ModelSerializer):
 
    class Meta:
        model = Ubicacion
        fields = ['nombre']
    
    def validate_nombre(self,nombre):
        ubicacionNombre = Ubicacion.objects.filter(nombre=nombre).first()
        if(not ubicacionNombre is None and ubicacionNombre.id != self.instance.id):
            raise serializers.ValidationError('Ya existe una ubicacion con ese nombre')
        return nombre


class UsuarioSerializerRegistro(serializers.Serializer):
 
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField()
    rol = serializers.IntegerField()
    edad = serializers.IntegerField()
    sexo = serializers.CharField()
    
    def validate_username(self,username):
        usuario = UserLogin.objects.filter(username=username).first()
        if(not usuario is None):
            raise serializers.ValidationError('Ya existe un usuario con ese nombre')
        return username
    
################################# PARTIDOS #####################################

class PartidoSerializer(serializers.ModelSerializer):
    
    equipo_local = EquipoSerializer()
    
    class Meta():
        model = Partido
        fields = ['fecha','ubicacion','equipo_local','equipo_visitante','color_local','color_visitante','puntos_local','puntos_visitante']
        
    
class PartidoSerializerCreate(serializers.ModelSerializer):

    class Meta():
        model = Partido
        fields = ['fecha','ubicacion','equipo_local','equipo_visitante','color_local','color_visitante','puntos_local','puntos_visitante']

    def validate_fecha(self,fecha):
        fecha = Partido.objects.filter(fecha=fecha).first()
        if (fecha <= datetime.now()):
            raise serializers.ValidationError('El partido no puede ser en una fecha anterior a hoy')
        return fecha
    
    def create(self,validated_data):
        
        if (validated_data['equipo_local'].color_eq_1 == validated_data['equipo_visitante'].color_eq_1):
            color_visitante = validated_data['equipo_visitante'].color_eq_2
                       
        partido = Partido.objects.create(
            fecha = validated_data['fecha'],
            ubicacion = validated_data['ubicacion'],
            equipo_local = validated_data['equipo_local'],
            equipo_visitante = validated_data['equipo_visitante'],
            color_local = validated_data['color_local'], 
            color_visitante = color_visitante,                 
            puntos_local = 0,
            puntos_visitante = 0,          
        )
        return partido