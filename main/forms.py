#encoding:utf-8
from django import forms
from main.models import Fuente, Plataforma
   
class BusquedaPorFuenteForm(forms.Form):
    lista = [(f.id,f.nombre) for f in Fuente.objects.all()]
    fuente = forms.ChoiceField(label="Seleccione la fuente", choices=lista, widget=forms.Select(attrs={'class':'custom-select select-maximo-ancho'}))

class BusquedaPorPlataformaForm(forms.Form):
    lista = [(p.id,p.acronimo) for p in Plataforma.objects.all()]
    plataforma = forms.ChoiceField(label="Seleccione la plataforma", choices=lista, widget=forms.Select(attrs={'class':'custom-select select-maximo-ancho'}))

class BusquedaPorFabricanteForm(forms.Form):
    lista = [(f[0],f[0]) for f in Plataforma.objects.order_by().values_list('fabricante').distinct()]
    fabricante = forms.ChoiceField(label="Seleccione el fabricante", choices=lista, widget=forms.Select(attrs={'class':'custom-select select-maximo-ancho'}))

class BusquedaPorTextoForm(forms.Form):
    texto = forms.CharField(label='Texto a buscar', max_length=100, widget=forms.TextInput(attrs={'class':'form-control select-maximo-ancho'}))