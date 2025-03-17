from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings  

class Usuario(AbstractUser):
    nome_completo = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    
    
    def __str__(self):
        return self.nome_completo

 
class Livro(models.Model):
    nome = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='livros/', blank=True, null=True)
    genero = models.CharField(max_length=100)
    detalhes = models.TextField()  
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Mensagem(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    usuario_remetente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    usuario_destinatario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    conteudo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    def __str__(self):
        return f"De {self.usuario_remetente.username} para {self.usuario_destinatario.username} sobre {self.livro.nome}"