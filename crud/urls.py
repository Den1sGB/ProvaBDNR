from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('eventos/novo/', views.cria_evento, name='cria_evento'),
    path('eventos/editar/<int:id>/', views.atualiza_evento, name='atualiza_evento'),
    path('eventos/deletar/<int:id>/', views.deleta_evento, name='deleta_evento'),
    path('login/', views.login_view, name='login'),
    path('chat/<int:evento_id>/', views.chat_view, name='chat'),
]
