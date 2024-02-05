from django.forms import ModelForm
from django import forms
from .models import *
from datetime import date
import datetime
from django.contrib.auth.forms import UserCreationForm


class BusquedaEquipoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    

class BusquedaAvanzadaEquipoForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False)
    capacidad = forms.IntegerField(required=False)

    def clean(self):
        super().clean()
        
        #Obtenemos los campos
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        capacidad = self.cleaned_data.get('capacidad')

        if(textoBusqueda == ""):
             self.add_error('textoBusqueda', 'no textoBusqueda')
        
        if(capacidad < 0):
             self.add_error('capacidad', 'no capacidad')
        
        return self.cleaned_data