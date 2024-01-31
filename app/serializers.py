from rest_framework import serializers
from .models import *

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipos
        fields = '__all__'