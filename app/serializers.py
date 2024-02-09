from rest_framework import serializers
from .models import *


################################## USUARIOS ######################################

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta():
        model = UserLogin
        fields = ['first_name','last_name']
        
class UsuariosSerializer(serializers.ModelSerializer):
    
    rol = UserLoginSerializer()
    
    class Meta():
        model = Usuarios
        fields = '__all__'

#################################### LIGA ######################################

class LigaSerializer(serializers.ModelSerializer):
    class Meta():
        model = Liga
        fields = ['id','liga']
        
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
    
    
        
        
################################## EQUIPO ######################################
       
class EquipoSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Equipos
        fields=['nombre','deporte','liga','capacidad']
        
    def validate_nombre(self,nombre):
        equipoNombre = Equipos.objects.filter(nombre=nombre).first()
        
        if(not equipoNombre is None):
            if(not self.instance is None and equipoNombre.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('Ya existe un equipo con ese nombre')
        return nombre
    
    def validate_capacidad(self, capacidad):
        if(self.initial_data['deporte'] == 'BSK'):
            pass
        elif(self.initial_data['deporte'] == 'FUT'):
            pass
        elif (self.initial_data['deporte'] == 'PDL'):
            pass
        return capacidad

class EquipoSerializer(serializers.ModelSerializer):
    
    usuario = UsuariosSerializer(many=True)
    liga = LigaSerializer()
    deporte = DeporteSerializer()
    
    class Meta:
        model = Equipos
        fields = ['id','nombre','deporte','liga','capacidad','usuario']
        
        
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
    
    
