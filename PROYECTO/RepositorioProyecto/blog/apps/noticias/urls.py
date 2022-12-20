from django.urls import path
from . import views

app_name = 'noticias'

urlpatterns = [

    path('', views.Listar_Noticias, name='listar'),

    path('Detalle/<int:pk>', views.Detalle_Noticias, name='detalle'),

    path('Todas/<int:pg>/<int:pk>', views.Todas_by, name='todas'),

    path('Comentario/', views.Comentar_Noticia, name='comentar'),

]
