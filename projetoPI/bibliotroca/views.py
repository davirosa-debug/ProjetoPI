from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Usuario
from django.contrib.auth.hashers import make_password




# Página de login
def logar(request):
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["senha"]

        user = authenticate(request, username=email, password=senha)
        if user is not None:
            logar(request, user)
            return redirect("sessao")  # Redireciona para a sessão após login
        else:
            return render(request, "login.html", {"error": "E-mail ou senha inválidos"})

    return render(request, "login.html")

# Página protegida (sessão)
@login_required
def sessao(request):
    return render(request, "sessao.html")

# Logout do usuário
def sair(request):
    logout(request)
    return redirect("logar")




# Página inicial
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Usuario #Importe seu modelo Usuario

def home(request):
    return render(request, 'home.html')

def cadastrar(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        email = request.POST["email"]
        senha = request.POST["senha"]

        if Usuario.objects.filter(email=email).exists():
            return render(request, "cadastro.html", {"error": "E-mail já cadastrado"})

        try:
            usuario = Usuario.objects.create_user( #alteração aqui
                username=email,
                email=email,
                password=senha,
                nome_completo=nome #alteração aqui
            )
            login(request, usuario)
            return redirect("sessao")
        except Exception as e:
            print(f"Erro ao cadastrar usuário: {e}")
            return render(request, "cadastro.html", {"error": "Erro ao cadastrar usuário. Tente novamente."})

    return render(request, "cadastro.html")