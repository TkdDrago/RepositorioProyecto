from django.shortcuts import render
from django.shortcuts import redirect
from apps.noticias.models import Categoria
# request ' es un diccionario que continuamente se va pasando entre el navegador y el servidor'


def Home(request):
    return redirect('/Noticias')


def Nosotros(request):
    contexto = {}
    contexto['categorias'] = Categoria.objects.all().order_by('nombre')

    return render(request, 't_nosotros.html', contexto)
