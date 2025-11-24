from django.db import models
from django.contrib.auth.models import User


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100, blank=True)
    codigo = models.CharField(max_length=50, unique=True)
    quantidade_total = models.PositiveIntegerField(default=1)
    quantidade_disponivel = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.titulo


class SalaEstudo(models.Model):
    nome = models.CharField(max_length=100)
    capacidade = models.PositiveIntegerField(default=1)
    localizacao = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nome


class Emprestimo(models.Model):
    STATUS = (
        ('ABERTO', 'Aberto'),
        ('DEVOLVIDO', 'Devolvido'),
        ('ATRASADO', 'Atrasado'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_emprestimo = models.DateField(auto_now_add=True)
    data_devolucao_prevista = models.DateField()
    data_devolucao_real = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='ABERTO')

    def __str__(self):
        return f'{self.livro.titulo} - {self.usuario.username}'


class ReservaSala(models.Model):
    STATUS = (
        ('AGENDADA', 'Agendada'),
        ('CANCELADA', 'Cancelada'),
        ('FINALIZADA', 'Finalizada'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    sala = models.ForeignKey(SalaEstudo, on_delete=models.CASCADE)
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS, default='AGENDADA')

    def __str__(self):
        return f'{self.sala.nome} - {self.usuario.username}'


class PerfilUsuario(models.Model):
    TIPO_CHOICES = (
        ('ALUNO', 'Aluno'),
        ('FUNCIONARIO', 'Funcionário'),
    )

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil'
    )
    matricula = models.CharField(max_length=50)
    login = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='ALUNO')

    def __str__(self):
        return f'{self.usuario.username} - {self.tipo}'
