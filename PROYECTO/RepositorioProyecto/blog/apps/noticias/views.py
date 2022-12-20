from django.contrib.auth.decorators import login_required
from .models import Noticia, Categoria, Comentario
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from random import sample, choice
from django.core.paginator import Paginator
import pandas as pd

categories_selected = []

# 4 NOTICIAS DE UNA MISMA CATEGORÍA


def by_category_news(cat, n):
    count = 0
    noticia_categoria = []
    while True:
        # DE NO HABER 4 NOTICIAS DE UNA MISMA CATEGORÍA
        # SE TOMAN 4 NOTICIAS RANDOM
        if (count >= len(cat)):
            numbers = sample(range(len(n)), 4)
            noticia_categoria = [n[i] for i in numbers]
            break

        # VERIFICA SI HAY 4 NOTICIAS EN UNA MISMA CATEGORÍA
        elif (len(noticia_categoria) < 4):
            counter = 0
            while True:
                if counter >= len(cat):
                    break

                category = choice(cat)
                if not category in categories_selected:
                    categories_selected.append(category)
                    break
                counter += 1
            noticia_categoria = Noticia.objects.filter(
                categoria_noticia=category)
        count += 1
    return noticia_categoria

# SECCIÓN LISTAR NOTICIAS


def Listar_Noticias(request):
    contexto = {}

    id_categoria = request.GET.get('id', None)

    if id_categoria:
        n = Noticia.objects.filter(categoria_noticia=id_categoria)
    else:
        # LISTA DE NOTICIAS Y LISTA DE CATEGORÍAS
        n = Noticia.objects.all()
        cat = Categoria.objects.all().order_by('nombre')

        # 4 NOTICIAS ALEATORIAS SIN REPETIR INDICE
        numbers = sample(range(len(n)), 4)
        noticias_random = [n[i] for i in numbers]

        # 3 NOTICIAS PÚBLICADAS RECIENTEMENTE
        noticias_recientes = []
        df = pd.DataFrame({"fecha": [n[i].fecha for i in range(len(n))]})
        df_desending = df.sort_values(
            by="fecha", ascending=False).values.tolist()[:4]
        for i in df_desending:
            for j in range(len(n)):
                if i[0] == n[j].fecha:
                    noticias_recientes.append(n[j])
                    break

        noticia_categoria_1 = by_category_news(cat, n)
        noticia_categoria_2 = by_category_news(cat, n)
        noticia_categoria_3 = by_category_news(cat, n)

        # 8(MAX) NOTICIAS MÁS VISTAS
        n_ascending = sorted(n, key=lambda k: k.views_total)[:8]
        noticias_mas_vistas = reversed(n_ascending)

    contexto['noticias'] = n
    contexto['noticias_random'] = noticias_random
    contexto['noticias_categoria_1'] = noticia_categoria_1
    contexto['noticias_categoria_2'] = noticia_categoria_2
    contexto['noticias_categoria_3'] = noticia_categoria_3
    contexto['ultimas_noticias'] = noticias_recientes
    contexto['noticias_destacadas'] = noticias_mas_vistas
    contexto['categorias'] = cat

    return render(request, 'noticias/listar.html', contexto)


# SECCIÓN DETALLE DE NOTICIA
def Detalle_Noticias(request, pk):
    contexto = {}

    cat = Categoria.objects.all().order_by('nombre')
    n = Noticia.objects.get(pk=pk)  # RETORNA SOLO UN OBEJTO
    contexto['noticia'] = n
    contexto['categorias'] = cat

    c = Comentario.objects.filter(noticia=n)
    contexto['comentarios'] = c
    all_noticias = Noticia.objects.all()  # RETORNA UNA LISTA DE OBJETOS
    contexto['noticias'] = all_noticias

    session_key = 'viewed_{}'.format(pk)

    # incrementa el número de visitas en el modelo, se permite solo 1 visita por usuario, el permiso se restea después de 1 semana.
    if not request.session.get(session_key, False):
        n.views_total = n.views_total + 1
        n.views_week = n.views_week + 1
        n.save()
        request.session[session_key] = True

    return render(request, 'noticias/detalle.html', contexto)

# SECCIÓN TODAS LAS NOTICIAS POR CATEGORÍA


def Todas_by(request, pg, pk):
    contexto = {}
    cat = Categoria.objects.all().order_by('nombre')

    if pk:
        n = Noticia.objects.filter(categoria_noticia=pk)
        cat_filter = cat.filter(pk=pk)[0].nombre
    else:
        n = Noticia.objects.all()
        cat_filter = ''

    p = Paginator(n, 4)
    pages_pagination = p.num_pages
    page1 = p.page(pg)

    contexto['noticias'] = page1.object_list
    contexto['pagination_number'] = pg
    contexto['range'] = range(pages_pagination)
    contexto['pagination_pages'] = pages_pagination
    contexto['categorias'] = cat
    contexto['categoria_noticia'] = cat_filter
    contexto['pk'] = pk

    return render(request, 'noticias/todas.html', contexto)


@ login_required
def Comentar_Noticia(request):

    com = request.POST.get('comentario', None)
    usu = request.user
    noti = request.POST.get('id_noticia', None)  # OBTENGO LA PK
    noticia = Noticia.objects.get(pk=noti)  # BUSCO LA NOTICIA CON ESA PK
    noticia.comentarios += 1
    noticia.save()
    coment = Comentario.objects.create(usuario=usu, noticia=noticia, texto=com)

    return redirect(reverse_lazy('noticias:detalle', kwargs={'pk': noti}))

# {'nombre':'nicolas', 'apellido':'Tortosa', 'edad':33}
# EN EL TEMPLATE SE RECIBE UNA VARIABLE SEPARADA POR CADA CLAVE VALOR
# nombre
# apellido
# edad


'''
ORM
CLASE.objects.get(pk = ____)
CLASE.objects.filter(campos = ____)
CLASE.objects.all() ---> SELECT * FROM CLASE
'''
