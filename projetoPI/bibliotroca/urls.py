from django.urls import path
from . import views
from bibliotroca.views import cadastrar_livro


urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('logar/', views.logar, name='logar'),
    path('sair/', views.sair, name='sair'),
    path('cadastrar_livro/', views.cadastrar_livro, name='cadastrar_livro'),
    path('livros/', views.livros, name='livros'),
    path('livros/<int:livro_id>/', views.detalhes_livro, name='detalhes_livro'),
    path('livros/<int:livro_id>/excluir/', views.excluir_livro, name='excluir_livro'),
    path('livros/<int:livro_id>/enviar-mensagem-publica/', views.enviar_mensagem_publica, name='enviar_mensagem_publica'),
    path('livros/<int:pk>/enviar-mensagem/', views.enviar_mensagem_privada, name='enviar_mensagem_privada'),
    path('mensagens/', views.mensagens_recebidas, name='mensagens_recebidas'),
    path('responder/<int:remetente_id>/', views.responder_mensagem, name='responder_mensagem'),
    path('mensagens/', views.mensagens_recebidas, name='mensagens_recebidas'),
    path('mensagens/responder/<int:remetente_id>/', views.responder_mensagem, name='responder_mensagem'),
    path('mensagens/excluir/<int:pk>/', views.excluir_mensagem, name='excluir_mensagem'),

]