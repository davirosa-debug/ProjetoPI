from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Livro, Mensagem, Usuario
from .forms import LivroForm
from .models import Livro, Mensagem, MensagemPrivada
from .forms import EnviarMensagemForm
from django.db import models
from .forms import ResponderMensagemForm
from .forms import EnviarMensagemForm
from django.contrib.auth import get_user_model
Usuario = get_user_model()

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
            return redirect("home")
        else:
            return render(request, "registration/login.html", {"error": "E-mail ou senha inválidos"})

    return render(request, "registration/login.html")



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
    messages_to_display = list(messages.get_messages(request))
    print(f"Número de mensagens na sessão ao carregar livros: {len(messages_to_display)}")  
    return render(request, 'livros.html', {'livros': livros, 'messages_to_display': messages_to_display})

@login_required
def enviar_mensagem_publica(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            conteudo = request.POST.get('mensagem')
            if conteudo:
                Mensagem.objects.create(
                    livro=livro,
                    usuario_remetente=request.user,
                    usuario_destinatario=livro.usuario, 
                    conteudo=conteudo
                )
                return redirect('detalhes_livro', livro_id=livro_id)
            else:
                messages.warning(request, "A mensagem não pode estar vazia.")
        else:
            messages.warning(request, "Efetue o login para enviar mensagens.")
    return redirect('detalhes_livro', livro_id=livro_id)


@login_required
@login_required
def mensagens_recebidas(request):
    mensagens = MensagemPrivada.objects.filter(destinatario=request.user).order_by('-criado_em')
    form = EnviarMensagemForm()

    if request.method == 'POST':
        form = EnviarMensagemForm(request.POST)
        if form.is_valid():
            remetente_id = request.POST.get('remetente_id')
            if remetente_id:
                try:
                    remetente = Usuario.objects.get(pk=remetente_id)
                    if remetente == request.user:
                        messages.warning(request, "Você não pode enviar mensagens para si mesmo.")
                    else:
                        MensagemPrivada.objects.create(
                            remetente=request.user,
                            destinatario=remetente,
                            conteudo=form.cleaned_data['conteudo']
                        )
                        messages.success(request, f"Resposta para {remetente.nome_completo} enviada com sucesso!")
                        form = EnviarMensagemForm()
                except Usuario.DoesNotExist:
                    messages.error(request, "Usuário remetente não encontrado.")
                except Exception as e:
                    messages.error(request, f"Erro ao enviar resposta: {e}")
            else:
                messages.error(request, "ID do remetente não fornecido.")
        # O formulário precisa ser passado para o contexto sempre

    context = {
        'mensagens': mensagens,
        'form': form,
    }
    return render(request, 'mensagens_recebidas.html', context)

@login_required
def excluir_mensagem(request, pk):
    mensagem = get_object_or_404(MensagemPrivada, pk=pk, destinatario=request.user)
    if request.method == 'POST':  
        mensagem.delete()
        messages.success(request, "Mensagem excluída com sucesso!")
        return redirect('mensagens_recebidas')
    
    elif request.method == 'GET':
        mensagem.delete()
        messages.success(request, "Mensagem excluída com sucesso!")
        return redirect('mensagens_recebidas')
    
@login_required
def enviar_mensagem_privada(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        form = EnviarMensagemForm(request.POST)
        if form.is_valid():
            destinatario = livro.usuario
            if request.user == destinatario:
                messages.warning(request, )
            else:
                MensagemPrivada.objects.create(
                    remetente=request.user,
                    destinatario=destinatario,
                    conteudo=form.cleaned_data['conteudo']
                )
                messages.success(request, "Mensagem privada enviada com sucesso!")
                return redirect('detalhes_livro', livro_id=pk)
        else:
            messages.error(request, "Erro ao enviar mensagem privada.")
    return redirect('detalhes_livro', livro_id=pk)



@login_required
def home(request):
    livros = Livro.objects.all()
    if request.user.is_authenticated:
        mensagens_nao_lidas = MensagemPrivada.objects.filter(
            destinatario=request.user,
            lida=False
        ).count()
    else:
        mensagens_nao_lidas = 0
    return render(request, 'home.html', {'livros': livros, 'mensagens_nao_lidas': mensagens_nao_lidas})

@login_required
def responder_mensagem(request, remetente_id):
    remetente = get_object_or_404(Usuario, pk=remetente_id)
    if request.method == 'POST':
        form = EnviarMensagemForm(request.POST)
        if form.is_valid():
            MensagemPrivada.objects.create(
                remetente=request.user,
                destinatario=remetente,
                conteudo=form.cleaned_data['conteudo']
            )
            messages.success(request, f"Resposta para {remetente.nome_completo} enviada com sucesso!")
            return redirect('mensagens_recebidas') # Ou para outra página relevante
        else:
            messages.error(request, "Erro ao enviar resposta.")
    else:
        form = EnviarMensagemForm()
    return render(request, 'responder_mensagem.html', {'form': form, 'remetente': remetente})




@login_required
def detalhes_livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    mensagens_publicas = Mensagem.objects.filter(livro=livro).order_by('data_envio')
    mensagens_privadas = MensagemPrivada.objects.filter(
        (models.Q(remetente=request.user, destinatario=livro.usuario) |
         models.Q(remetente=livro.usuario, destinatario=request.user))
    ).order_by('id')

    if request.user == livro.usuario:
        Mensagem.objects.filter(livro=livro, usuario_destinatario=request.user, lida=False).update(lida=True)

    if request.method == 'POST':
        form = EnviarMensagemForm(request.POST)
        if form.is_valid():
            MensagemPrivada.objects.create(
                remetente=request.user,
                destinatario=livro.usuario,
                conteudo=form.cleaned_data['conteudo']
            )
            return redirect('detalhes_livro', livro_id=livro_id)
        else:
            messages.warning(request, "Erro ao enviar mensagem.")
    else:
       
        form = EnviarMensagemForm(initial={'destinatario': livro.usuario})

    return render(request, 'detalhes_livro.html', {'livro': livro, 'mensagens_publicas': mensagens_publicas, 'mensagens_privadas': mensagens_privadas, 'form': form})

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

def home(request):
    livros = Livro.objects.all()
    if request.user.is_authenticated:
        mensagens_nao_lidas = MensagemPrivada.objects.filter(
            destinatario=request.user,
            lida=False
        ).count()
    else:
        mensagens_nao_lidas = 0
    return render(request, 'home.html', {'livros': livros, 'mensagens_nao_lidas': mensagens_nao_lidas})


