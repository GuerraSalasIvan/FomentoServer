from rest_framework import serializers
from .models import *

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta():
        model = UserLogin
        fields = ['first_name']
        
class UsuariosSerializer(serializers.ModelSerializer):
    
    rol = UserLoginSerializer()
    
    class Meta():
        model = Usuarios
        fields = '__all__'

class LigaSerializer(serializers.ModelSerializer):
    class Meta():
        model = Liga
        fields = ['liga']

class EquipoSerializer(serializers.ModelSerializer):
    
    usuario = UsuariosSerializer(many=True)
    liga = LigaSerializer()
    
    class Meta:
        model = Equipos
        fields = ['nombre','deporte','liga','capacidad','usuario']
        