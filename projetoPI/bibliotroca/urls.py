
from django.urls import path
from .views import home, cadastrar, logar,sessao,sair


urlpatterns = [
    path('', home, name='home'),  # Página inicial
    path('cadastro/', cadastrar, name='cadastro'),
    path('logar/', logar, name='logar'),
    path('sessao/', sessao, name='sessao'),
    path('sair/', sair, name='sair'),]