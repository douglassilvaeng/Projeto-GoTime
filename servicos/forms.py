from django import forms
from .models import Servico

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'preco', 'duracao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do serviço'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição do serviço'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor (R$)'}),
            'duracao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duração em minutos'}),
        }
from django import forms
from .models import Servico, HorarioDisponivel, Agendamento

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'preco', 'duracao']


class HorarioForm(forms.ModelForm):
    class Meta:
        model = HorarioDisponivel
        fields = ['servico', 'data', 'hora']


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['servico', 'horario']
