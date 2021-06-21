#encoding:utf-8
from django.contrib import admin
from main.models import Fuente, Plataforma, Noticia, Actualizacion



class FuenteAdmin(admin.ModelAdmin):
    list_filter = ("idioma",)
    list_display = ("nombre", "direccion_web", "idioma")

class PlataformaAdmin(admin.ModelAdmin):
    list_filter = ("fabricante",)
    list_display = ("acronimo", "nombres", "fabricante")

class NoticiaAdmin(admin.ModelAdmin):
    list_filter = ("fuente", "plataforma", "fecha")
    list_display = ("titulo", "fuente", "fecha")

admin.site.register(Fuente, FuenteAdmin)
admin.site.register(Plataforma, PlataformaAdmin)
admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Actualizacion)