from django.shortcuts import render
from main.models import Noticia, Actualizacion, Fuente, Plataforma
from main.forms import BusquedaPorFuenteForm, BusquedaPorPlataformaForm, BusquedaPorFabricanteForm, BusquedaPorTextoForm
from django.conf import settings
from django.core.paginator import Paginator
from bs4 import BeautifulSoup
import os
import urllib.request
import datetime
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.qparser import QueryParser, OrGroup
from whoosh.index import create_in,open_dir


def get_schema():
    return Schema(id_noticia=NUMERIC(stored=True), texto_noticia=TEXT(stored=True))

def fecha_string_to_datetime(fecha):
    fecha_lista_t = fecha.split('T')
    fecha_lista_hora_minuto = fecha_lista_t[1].split(':')
    fecha_string = fecha_lista_t[0] + " " + fecha_lista_hora_minuto[0] + ":" + fecha_lista_hora_minuto[1]
    datetime_object = datetime.datetime.strptime(fecha_string, '%Y-%m-%d %H:%M')
    print(datetime_object)
    return datetime_object

def get_enlaces_vadal():
    print("Entra en enlaces vandal")
    enlace = "https://vandal.elespanol.com/noticias/videojuegos/"
    f = urllib.request.urlopen(enlace)
    s = BeautifulSoup(f,"lxml")
    enlaces_vandal = []
    titulos_caja = s.find("div", id="pestana_noticias").find_all("h2", class_="titulocaja")
    for titulo_caja in titulos_caja:
        enlaces_vandal.append(titulo_caja.find_parent("a")['href'])
    return enlaces_vandal

def get_enlaces_3djuegos():
    enlace = "https://www.3djuegos.com/novedades/noticias/juegos/0f0f0f0/fecha/"
    f = urllib.request.urlopen(enlace)
    s = BeautifulSoup(f,"lxml")
    enlaces_3djuegos = []
    lista_noticias = s.find("ul", class_="list_nov mar_b16").find_all("h2")
    for ln in lista_noticias:
        enlaces_3djuegos.append(ln.find("a")['href'])
    return enlaces_3djuegos

def get_enlaces_meristation():
    f = urllib.request.urlopen("https://as.com/meristation/noticias/")
    s = BeautifulSoup(f,"lxml")

    enlaces_meristation = []
    divrow1 = s.find("div", class_="ct ct-main").find_all("div", class_="row")[1].find("div").find_all("div", class_="row")[1].find_all("h2")
    for dr in divrow1:
        enlaces_meristation.append(dr.find("a")['href'])
    
    return enlaces_meristation

def get_noticias_vandal(enlaces_vandal):
    for e in enlaces_vandal:
        f = urllib.request.urlopen(e)
        s = BeautifulSoup(f,"lxml")

        titulo = s.find("h1", itemprop="headline").text.strip()
        subtitulo = s.find("span", class_="summary").text.strip()
        fecha_texto = s.find("span", class_="value-title")['title']
        fecha_final = fecha_string_to_datetime(fecha_texto)

        try:
            plataformas = []
            plataformas_spans = s.find("td", class_="juegos").find_all("span", class_="falsolink")
            for plataforma_span in plataformas_spans:
                plataformas.append(plataforma_span.find("span").text.strip())
        except:
            plataformas = []
    
        fuente = Fuente.objects.get(nombre="Vandal")

        lista_plataformas_obj = []
        for plataforma in plataformas:
            try:
                plataforma_obj = Plataforma.objects.get(nombres__icontains=plataforma)
                lista_plataformas_obj.append(plataforma_obj)
            except:
                print("Plataforma no existente en la BBDD")

        noticia_obj = Noticia.objects.create(titulo = titulo, subtitulo = subtitulo,
                                enlace = e, fuente = fuente, fecha = fecha_final)
    
        for lp in lista_plataformas_obj:
            noticia_obj.plataforma.add(lp)



def get_noticias_3Djuegos(enlaces_3djuegos):
    for e in enlaces_3djuegos:
        if "https://www.3djuegos.com/" in e:
            f = urllib.request.urlopen(e)
            s = BeautifulSoup(f,"lxml")


            titulo = s.find("div", id="div_cuerpo_noticia").find("h1").text.strip()
            subtitulo = s.find("div", id="div_cuerpo_noticia").find("p").text.strip()
            fuente = Fuente.objects.get(nombre="3DJuegos")
            fecha_texto = s.find("time")['datetime']
            fecha_final = fecha_string_to_datetime(fecha_texto)

            try:
                plataformas = []
                plataformas_spans = s.find("div", class_="caja_j_rela").find("div", class_="s14").find("p", class_="mar_t2").find_all("span")
                for plataformas_span in plataformas_spans:
                        plataformas.append(plataformas_span.text.strip())
            except:
                plataformas = []

            lista_plataformas_obj = []
            for plataforma in plataformas:
                try:
                    plataforma_obj = Plataforma.objects.get(nombres__icontains=plataforma)
                    lista_plataformas_obj.append(plataforma_obj)
                except:
                    print("Plataforma no existente en la BBDD")
            
            noticia_obj = Noticia.objects.create(titulo = titulo, subtitulo = subtitulo,
                                        enlace = e, fuente = fuente, fecha = fecha_final)

            for lp in lista_plataformas_obj:
                    noticia_obj.plataforma.add(lp)

def get_noticias_meristation(enlaces_meristation):
    for e in enlaces_meristation:
        f = urllib.request.urlopen(e)
        s = BeautifulSoup(f,"lxml")

        titulo = s.find("h1", class_="art-tl h-xl").text.strip()
        try:
            subtitulo = s.find("h2", class_="art-stl").text.strip()
        except:
            subtitulo = titulo
        fuente = Fuente.objects.get(nombre = "Meristation")
        fecha_texto = s.find("time", class_="art-date")['datetime']
        fecha_final = fecha_string_to_datetime(fecha_texto)
        lista_etiquetas_lis = s.find("ul", class_="art-tags-li").find_all("li")
        
        lista_etiquetas = []
        for le in lista_etiquetas_lis:
            lista_etiquetas.append(le.text.strip())

        lista_plataformas_obj = []
        for plataforma in lista_etiquetas:
                try:
                    plataforma_obj = Plataforma.objects.get(nombres__icontains=plataforma)
                    lista_plataformas_obj.append(plataforma_obj)
                except:
                    donothing = 0

        noticia_obj = Noticia.objects.create(titulo = titulo, subtitulo = subtitulo,
                                        enlace = e, fuente = fuente, fecha = fecha_final)
        
        for lp in lista_plataformas_obj:
                noticia_obj.plataforma.add(lp)

def populateDB():
    
    Noticia.objects.all().delete()

    enlaces_vandal = get_enlaces_vadal()
    get_noticias_vandal(enlaces_vandal)

    enlaces_3djuegos = get_enlaces_3djuegos()
    get_noticias_3Djuegos(enlaces_3djuegos)
    
    enlaces_meristation = get_enlaces_meristation()
    get_noticias_meristation(enlaces_meristation)

    Actualizacion.objects.all().delete()
    Actualizacion.objects.create(fecha = datetime.datetime.now().replace(tzinfo=None))

    


def inicio(request):
    noticias = Noticia.objects.all().order_by('-fecha')
    actualizacion_realizada = "no"

    paginator = Paginator(noticias, 9)
    page = request.GET.get('page')
    
    noticias = paginator.get_page(page)

    if request.method=='POST':
        if 'Actualizar' in request.POST:      
            #print("Le has dado a actualizar")
            populateDB()
            actualizacion_realizada = "si"

    actualizacion = Actualizacion.objects.all().order_by('-fecha')[0:1]
    fecha_actualizacion = actualizacion[0].fecha.replace(tzinfo=None)
    fecha_actual = datetime.datetime.now().replace(tzinfo=None)
    diferencia = fecha_actual - fecha_actualizacion
    ultimaActualizacion = ""
    if(diferencia.days > 0):
        ultimaActualizacion = "hace más de un día"
    else:
        if(((diferencia.total_seconds() / 3600)-2) > 2):
            ultimaActualizacion = "hace más de dos horas"
        else:
            ultimaActualizacion = "hace menos de dos horas"

    return render(request,'inicio.html',{'noticias': noticias, 'MEDIA_URL': settings.MEDIA_URL, 'ultimaActualizacion':ultimaActualizacion, 'actualizacion_realizada': actualizacion_realizada})


def sobre(request):
        return render(request,'sobre.html',{'MEDIA_URL': settings.MEDIA_URL})

def noticias_por_fuente(request):
        formulario = BusquedaPorFuenteForm()
        noticias = []
        fuente_texto = ""

        if request.method=='GET':
            formulario = BusquedaPorFuenteForm(request.GET)      
            if formulario.is_valid():
                fuente = Fuente.objects.get(id = formulario.cleaned_data['fuente'])
                noticias = Noticia.objects.filter(fuente = fuente).order_by('-fecha')
        fuente_texto = request.GET.get('fuente')
        paginator = Paginator(noticias, 9)
        page = request.GET.get('page')
        noticias = paginator.get_page(page)

        return render(request,'noticiasporweb.html',{'MEDIA_URL': settings.MEDIA_URL, 'formulario':formulario, 'noticias':noticias, 'fuente_get':fuente_texto})

def noticias_por_plataforma(request):
        formulario = BusquedaPorPlataformaForm()
        noticias = []
        plataforma_texto = ""

        if request.method=='GET':
            formulario = BusquedaPorPlataformaForm(request.GET)      
            if formulario.is_valid():
                plataforma = Plataforma.objects.get(id = request.GET.get('plataforma'))
                noticias = plataforma.noticia_set.all().order_by('-fecha')

        plataforma_texto = request.GET.get('plataforma')
        paginator = Paginator(noticias, 9)
        page = request.GET.get('page')
        noticias = paginator.get_page(page)

        return render(request,'noticiasporplataforma.html',{'MEDIA_URL': settings.MEDIA_URL, 'formulario':formulario, 'noticias':noticias, 'plataforma_get':plataforma_texto})


def noticias_por_fabricante(request):
    formulario = BusquedaPorFabricanteForm()

    noticias = []
    fabricante_texto = ""

    if request.method=='GET':
            formulario = BusquedaPorFabricanteForm(request.GET)      
            if formulario.is_valid():
                plataformas = Plataforma.objects.filter(fabricante = request.GET.get('fabricante'))
                for p in plataformas:
                    noticias_plataforma = p.noticia_set.all().order_by('-fecha')
                    for n in noticias_plataforma:
                        if n not in noticias:
                            noticias.append(n)
    noticias.sort(key=lambda n: n.fecha,reverse=True)
    fabricante_texto = request.GET.get('fabricante')
    paginator = Paginator(noticias, 9)
    page = request.GET.get('page')
    noticias = paginator.get_page(page)


    return render(request,'noticiasporfabricante.html',{'MEDIA_URL': settings.MEDIA_URL, 'formulario': formulario, 'noticias':noticias, 'fabricante_get':fabricante_texto})

"""def noticias_por_texto(request):
        formulario = BusquedaPorTextoForm()
        noticias = []
        busqueda_texto = ""

        if request.method=='GET':
            formulario = BusquedaPorTextoForm(request.GET)      
            if formulario.is_valid():
                noticias = Noticia.objects.filter(titulo__icontains =  request.GET.get('texto')) | Noticia.objects.filter(subtitulo__icontains =  request.GET.get('texto'))
                noticias.order_by('-fecha')
        busqueda_texto = request.GET.get('texto')
        paginator = Paginator(noticias, 9)
        page = request.GET.get('page')
        noticias = paginator.get_page(page)

        return render(request,'busqueda.html',{'MEDIA_URL': settings.MEDIA_URL, 'formulario':formulario, 'noticias':noticias, 'texto_get':busqueda_texto})"""




def carga_whoosh(dirindex):
    if not os.path.exists(dirindex):
        os.mkdir(dirindex)
    
    ix = create_in(dirindex, schema=get_schema())
    writer = ix.writer()
    noticias = Noticia.objects.all()
    for n in noticias:
        plataformas = n.plataforma.all()
        plataforma_lista = " "
        fabricante_lista = " "
        for p in plataformas:
            plataforma_lista += "{} ".format(p.nombres)
            if p.fabricante not in fabricante_lista:
                fabricante_lista += "{} ".format(p.fabricante)
        texto_combinado = "{} {} {} {} {} {} {}".format(n.titulo, n.subtitulo, n.enlace, n.fuente.nombre, str(n.fecha), plataforma_lista, fabricante_lista)
        writer.add_document(id_noticia = n.id, texto_noticia = texto_combinado)
    writer.commit()
    

def noticias_por_texto(request):
    formulario = BusquedaPorTextoForm()
    busqueda_texto = ""
    dirindex = "index"
    carga_whoosh(dirindex)
    
    noticias = []
    
    if request.method=='GET':
        formulario = BusquedaPorTextoForm(request.GET)
        if str(request.GET.get('texto')).startswith('or(') and str(request.GET.get('texto')).endswith(')'):
            texto_a_buscar = request.GET.get('texto')[3:int(len(request.GET.get('texto')))-1]
            if formulario.is_valid():
                ix = open_dir(dirindex)
                with ix.searcher() as searcher:
                    query = QueryParser("texto_noticia", ix.schema,group=OrGroup).parse(request.GET.get('texto'))
                    results = searcher.search(query, limit=None)
                    for r in results:
                        noticias.append(Noticia.objects.get(id=r['id_noticia']))
        else:
            if formulario.is_valid():
                ix = open_dir(dirindex)
                with ix.searcher() as searcher:
                    query = QueryParser("texto_noticia", ix.schema).parse(request.GET.get('texto'))
                    results = searcher.search(query, limit=None)
                    for r in results:
                        noticias.append(Noticia.objects.get(id=r['id_noticia']))

    noticias.sort(key=lambda n: n.fecha,reverse=True)
    busqueda_texto = request.GET.get('texto')
    paginator = Paginator(noticias, 9)
    page = request.GET.get('page')
    noticias = paginator.get_page(page)

    return render(request,'busqueda.html',{'MEDIA_URL': settings.MEDIA_URL, 'formulario':formulario, 'texto_get':busqueda_texto,'noticias':noticias})