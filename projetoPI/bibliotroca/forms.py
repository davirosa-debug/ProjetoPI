from django import forms
from .models import Livro
from .models import Usuario

GENERO_CHOICES = [
    ('', 'Selecione o Gênero'),
    ('Ficcao', 'Ficção'),
    ('Romance', 'Romance'),
    ('Suspense', 'Suspense'),
    ('Terror', 'Terror'),
    ('Fantasia', 'Fantasia'),
    ('Ciencia Ficcao', 'Ciência Ficção'),
    ('Biografia', 'Biografia'),
    ('Autoajuda', 'Autoajuda'),
    ('Outros', 'Outros'),
]

class LivroForm(forms.ModelForm):
    genero = forms.ChoiceField(label='Gênero', choices=GENERO_CHOICES)

    class Meta:
        model = Livro
        fields = ['nome', 'foto', 'genero', 'detalhes'] 



class EnviarMensagemForm(forms.Form):
    conteudo = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Digite sua resposta'}))
    destinatario = forms.ModelChoiceField(queryset=Usuario.objects.all(), widget=forms.HiddenInput(), required=False)


class ResponderMensagemForm(forms.Form):
    conteudo = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Digite sua resposta'}))