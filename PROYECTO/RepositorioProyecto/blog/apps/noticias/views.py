from django.shortcuts import render

# Create your views here.

def Listar_Noticias(request):
    return render(request, 'noticias/listar.html')