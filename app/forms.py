from django.forms import ModelForm
from django import forms
from .models import *
from datetime import date
import datetime
from django.contrib.auth.forms import UserCreationForm


class BusquedaEquipoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    

#------------------------ Equipo ----------------------
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
    

#------------------------ Ubicacion ----------------------
class BusquedaAvanzadaUbicacionForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False)
    capacidad = forms.IntegerField(required=False)
    calle = forms.CharField(required=False)

    def clean(self):
        super().clean()
        
        #Obtenemos los campos
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        capacidad = self.cleaned_data.get('capacidad')
        calle = self.cleaned_data.get('calle')

        if(textoBusqueda == ""):
            self.add_error('textoBusqueda', 'no textoBusqueda')
        
        if(capacidad < 0):
            self.add_error('capacidad', 'no capacidad')
             
        if(calle == ""):
            self.add_error('calle', 'no calle')
        
        return self.cleaned_data
    
    
#------------------------ Perfil_publico ----------------------
class BusquedaAvanzadaPerfil_PublicoForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False)
    '''
    lugares = Perfil_Publico.objects.all()
    lugar_fav = forms.ModelMultipleChoiceField(
        queryset=lugares,
        required=True,
        help_text="Mantén pulsada la tecla control para seleccionar varios elementos"
    )
    '''
    
    

    def clean(self):
        super().clean()
        
        #Obtenemos los campos
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        #lugar_fav = self.cleaned_data.get('lugar_fav')

        if(textoBusqueda == ""):
            self.add_error('textoBusqueda', 'no textoBusqueda')
        '''
        if(lugar_fav < 0):
            self.add_error('lugar_fav', 'no lugar_fav')
        ''' 
        return self.cleaned_data