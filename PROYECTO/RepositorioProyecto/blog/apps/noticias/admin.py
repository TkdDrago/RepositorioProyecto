from django.contrib import admin

# Register your models here.
from .models import Categoria, Noticia

admin.site.register(Categoria)
admin.site.register(Noticia)
