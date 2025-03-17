from django.urls import path
from . import views
from bibliotroca.views import cadastrar_livro

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('logar/', views.logar, name='logar'),
    path('sessao/', views.sessao, name='sessao'),
    path('sair/', views.sair, name='sair'),
    path('cadastrar_livro/', views.cadastrar_livro, name='cadastrar_livro'),
    path('livros/', views.livros, name='livros'),
    path('livros/<int:livro_id>/', views.detalhes_livro, name='detalhes_livro'),
    path('livros/<int:livro_id>/excluir/', views.excluir_livro, name='excluir_livro'),
]