from django.db import models
from django.contrib.auth.models import User

# PERFIL (igual o seu)
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=200)
    cpf_cnpj = models.CharField(max_length=20)
    is_profissional = models.BooleanField(default=False)

    # 🔹 novo campo: quais serviços o profissional oferece
    servicos = models.ManyToManyField('Servico', blank=True, related_name='profissionais')

    def __str__(self):
        return f"{self.nome_completo} ({'Profissional' if self.is_profissional else 'Cliente'})"



# SERVIÇO (como já está)
class Servico(models.Model):
    profissional = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    duracao = models.IntegerField(help_text="Duração em minutos")

    def __str__(self):
        return self.nome


# HORÁRIOS DISPONÍVEIS (novo)
class HorarioDisponivel(models.Model):
    profissional = models.ForeignKey(User, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.servico.nome} - {self.data} às {self.hora}"


# AGENDAMENTO (novo)
class Agendamento(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agendamentos_cliente')
    profissional = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agendamentos_profissional')
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    horario = models.ForeignKey(HorarioDisponivel, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente.username} agendou {self.servico.nome} em {self.horario.data} às {self.horario.hora}"
