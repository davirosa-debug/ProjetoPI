from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Livro, Mensagem, Usuario
from .forms import LivroForm

from django.contrib import messages

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
            usuario = Usuario.objects.create_user(
                username=email,
                email=email,
                password=senha,
                nome_completo=nome
            )
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect("logar")
        except Exception as e:
            print(f"Erro ao cadastrar usuário: {e}")
            return render(request, "cadastro.html", {"error": "Erro ao cadastrar usuário. Tente novamente."})

    return render(request, "cadastro.html")

def logar(request):
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["senha"]

        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect("sessao")
        else:
            return render(request, "login.html", {"error": "E-mail ou senha inválidos"})

    return render(request, "login.html")

@login_required
def sessao(request):
    return render(request, "sessao.html")

def sair(request):
    logout(request)
    return redirect("logar")

@login_required
def cadastrar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.usuario = request.user
            livro.save()
            messages.success(request, "Livro cadastrado com sucesso!")
            return redirect('livros')
    else:
        form = LivroForm()
    return render(request, 'cadastrar_livro.html', {'form': form})

def livros(request):
    livros = Livro.objects.all().order_by('nome')
    return render(request, 'livros.html', {'livros': livros})

def detalhes_livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    mensagens = Mensagem.objects.filter(livro=livro).order_by('data_envio')

    if request.user == livro.usuario:
        Mensagem.objects.filter(livro=livro, usuario_destinatario=request.user, lida=False).update(lida=True)

    if request.method == 'POST':
        if request.user.is_authenticated:
            conteudo = request.POST.get('mensagem')
            if conteudo:
                Mensagem.objects.create(livro=livro, usuario_remetente=request.user, usuario_destinatario=livro.usuario, conteudo=conteudo)
                return redirect('detalhes_livro', livro_id=livro_id)
        else:
            messages.warning(request, "Efetue o login para enviar mensagens.")
            return redirect('logar')

    return render(request, 'detalhes_livro.html', {'livro': livro, 'mensagens': mensagens})

@login_required
def excluir_livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    if livro.usuario == request.user:
        livro.delete()
        messages.success(request, "Livro excluído com sucesso!")
        return redirect('livros')
    else:
        messages.error(request, "Você não tem permissão para excluir este livro.")
        return redirect('livros')


