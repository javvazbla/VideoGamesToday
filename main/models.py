#encoding:utf-8
from django.db import models
import pytz

class Fuente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, verbose_name='Nombre')
    direccion_web = models.CharField(max_length=250, verbose_name='Dirección Web')
    logotipo = models.ImageField(upload_to='logotipo', verbose_name='Logotipo')
    idioma = models.CharField(max_length=3, verbose_name='Idioma')

    def __str__(self):
        return self.nombre

class Plataforma(models.Model):
    id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=300, verbose_name='Nombres')
    acronimo = models.CharField(max_length=15, verbose_name='Acrónimo')
    fabricante = models.CharField(max_length=30, verbose_name='Fabricante')

    def __str__(self):
        return self.acronimo

class Noticia(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.TextField(verbose_name="Título")
    subtitulo = models.TextField(verbose_name="Subtítulo")
    enlace = models.CharField(max_length=250, verbose_name='enlace')
    fuente = models.ForeignKey(Fuente, on_delete=models.CASCADE)
    plataforma = models.ManyToManyField(Plataforma, blank = True)
    fecha = models.DateTimeField(verbose_name="Fecha", blank = True)

    def __str__(self):
        return self.titulo

class Actualizacion(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(verbose_name="Fecha")

    def __str__(self):
        return self.fecha.strftime("%m/%d/%Y, %H:%M:%S")