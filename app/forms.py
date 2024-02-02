from django.forms import ModelForm
from django import forms
from .models import *
from datetime import date
import datetime
from django.contrib.auth.forms import UserCreationForm


class BusquedaEquipoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)