from rest_framework import serializers
from .models import *

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta():
        model = UserLogin
        fields = ['first_name','last_name']
        
class UsuariosSerializer(serializers.ModelSerializer):
    
    rol = UserLoginSerializer()
    
    class Meta():
        model = Usuarios
        fields = '__all__'

class LigaSerializer(serializers.ModelSerializer):
    class Meta():
        model = Liga
        fields = ['liga']
        
class DeporteSerializer(serializers.ModelSerializer):
        
    class Meta():
        model = Deportes
        fields = '__all__'

class EquipoSerializer(serializers.ModelSerializer):
    
    usuario = UsuariosSerializer(many=True)
    liga = LigaSerializer()
    deporte = DeporteSerializer()
    
    class Meta:
        model = Equipos
        fields = ['id','nombre','deporte','liga','capacidad','usuario']
        
class UbicacionSerializer(serializers.ModelSerializer):
        
    class Meta():
        model = Ubicacion
        fields = '__all__'
        
class Perfil_PublicoSerializer(serializers.ModelSerializer):
        
    class Meta():
        model = Perfil_Publico
        fields = '__all__'
        
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
        