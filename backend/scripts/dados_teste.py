# INSERINDO DADOS DE TESTE
import os
import django

# CONFIGURA AMBIENTE DJANGO
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biblioteca_backend.settings")
django.setup()

from django.contrib.auth.models import User
from biblioteca.models import Livro, SalaEstudo, PerfilUsuario


# USUÁRIOS
def criar_usuarios():
    usuarios = [
        # ALUNOS
        {
            "matricula": "1001",
            "nome": "Ana Souza",
            "email": "ana.souza@example.com",
            "telefone": "11999990001",
            "senha": "senha123",
            "tipo": "ALUNO",
        },
        {
            "matricula": "1002",
            "nome": "Bruno Oliveira",
            "email": "bruno.oliveira@example.com",
            "telefone": "11999990002",
            "senha": "senha456",
            "tipo": "ALUNO",
        },
        {
            "matricula": "1003",
            "nome": "Carla Pereira",
            "email": "carla.pereira@example.com",
            "telefone": "11999990003",
            "senha": "senha789",
            "tipo": "ALUNO",
        },

        # FUNCIONÁRIOS
        {
            "matricula": "2001",
            "nome": "Daniel Costa",
            "email": "daniel.costa@example.com",
            "telefone": "11999990004",
            "senha": "func12345",
            "tipo": "FUNCIONARIO",
        },
        {
            "matricula": "2002",
            "nome": "Fernanda Lima",
            "email": "fernanda.lima@example.com",
            "telefone": "11999990005",
            "senha": "func54321",
            "tipo": "FUNCIONARIO",
        },
    ]

    print(">>> Criando usuários de teste...")

    for dados in usuarios:
        matricula = dados["matricula"]
        nome = dados["nome"]
        email = dados["email"]
        telefone = dados["telefone"]
        senha = dados["senha"]
        tipo = dados["tipo"]  # 'ALUNO' ou 'FUNCIONARIO'

        # Verifica se já existe um User com essa matrícula
        user, criado = User.objects.get_or_create(
            username=matricula,
            defaults={
                "first_name": nome,
                "email": email,
            },
        )

        if criado:
            user.set_password(senha)
        else:
            user.first_name = nome
            user.email = email
        if tipo == "FUNCIONARIO":
            user.is_staff = True

        user.save()

        perfil, _ = PerfilUsuario.objects.get_or_create(
            usuario=user,
            defaults={
                "matricula": matricula,
                "login": matricula,
                "telefone": telefone,
                "tipo": tipo,  # 'ALUNO' ou 'FUNCIONARIO'
            },
        )
        perfil.matricula = matricula
        perfil.login = matricula
        perfil.telefone = telefone
        perfil.tipo = tipo
        perfil.save()

        print(f" - Usuário {matricula} ({nome}) [{tipo}] OK")

    print(">>> Usuários criados/atualizados com sucesso!\n")


# LIVROS
def criar_livros():
    livros = [
        {
            "titulo": "O Pequeno Príncipe",
            "autor": "Antoine de Saint-Exupéry",
            "categoria": "Literatura",
            "codigo": "LIV001",
            "quantidade_total": 8,
        },
        {
            "titulo": "Dom Casmurro",
            "autor": "Machado de Assis",
            "categoria": "Literatura Brasileira",
            "codigo": "LIV002",
            "quantidade_total": 5,
        },
        {
            "titulo": "1984",
            "autor": "George Orwell",
            "categoria": "Ficção Científica",
            "codigo": "LIV003",
            "quantidade_total": 6,
        },
        {
            "titulo": "A Revolução dos Bichos",
            "autor": "George Orwell",
            "categoria": "Ficção",
            "codigo": "LIV004",
            "quantidade_total": 4,
        },
        {
            "titulo": "Clean Code",
            "autor": "Robert C. Martin",
            "categoria": "Programação",
            "codigo": "LIV005",
            "quantidade_total": 3,
        },
        {
            "titulo": "Código Limpo em Python",
            "autor": "Mariano Anaya",
            "categoria": "Programação",
            "codigo": "LIV006",
            "quantidade_total": 3,
        },
        {
            "titulo": "Algoritmos: Teoria e Prática",
            "autor": "Thomas H. Cormen",
            "categoria": "Computação",
            "codigo": "LIV007",
            "quantidade_total": 2,
        },
        {
            "titulo": "Use a Cabeça! Programação em Java",
            "autor": "Kathy Sierra, Bert Bates",
            "categoria": "Programação",
            "codigo": "LIV008",
            "quantidade_total": 4,
        },
        {
            "titulo": "Redes de Computadores",
            "autor": "Andrew S. Tanenbaum",
            "categoria": "Redes",
            "codigo": "LIV009",
            "quantidade_total": 3,
        },
        {
            "titulo": "Engenharia de Software",
            "autor": "Ian Sommerville",
            "categoria": "Engenharia de Software",
            "codigo": "LIV010",
            "quantidade_total": 3,
        },
    ]

    print(">>> Criando livros de teste...")

    for l in livros:
        codigo = l["codigo"]

        livro, criado = Livro.objects.get_or_create(
            codigo=codigo,
            defaults={
                "titulo": l["titulo"],
                "autor": l["autor"],
                "categoria": l["categoria"],
                "quantidade_total": l["quantidade_total"],
                "quantidade_disponivel": l["quantidade_total"],
            },
        )

        if not criado:
            livro.titulo = l["titulo"]
            livro.autor = l["autor"]
            livro.categoria = l["categoria"]
            livro.quantidade_total = l["quantidade_total"]
            livro.quantidade_disponivel = l["quantidade_total"]

        livro.save()
        print(f" - Livro {codigo} ({livro.titulo}) OK")

    print(">>> Livros criados/atualizados com sucesso!\n")


# SALAS DE ESTUDO (6 salas) --------

def criar_salas():
    """
    Cria 6 salas de estudo padrão.
    """

    salas = [
        {"nome": "Sala 01", "capacidade": 4},
        {"nome": "Sala 02", "capacidade": 6},
        {"nome": "Sala 03", "capacidade": 8},
        {"nome": "Sala 04", "capacidade": 10},
        {"nome": "Sala 05", "capacidade": 5},
        {"nome": "Sala 06", "capacidade": 12},
    ]

    print(">>> Criando salas de estudo...")

    for s in salas:
        sala, criado = SalaEstudo.objects.get_or_create(
            nome=s["nome"],
            defaults={
                "capacidade": s["capacidade"],
            },
        )

        if not criado:
            sala.capacidade = s["capacidade"]
            sala.save()

        print(f" - {sala.nome} (capacidade {sala.capacidade}) OK")

    print(">>> Salas criadas/atualizadas com sucesso!\n")


def main():
    criar_usuarios()
    criar_livros()
    criar_salas()
    print("Dados de teste populados com sucesso!")


if __name__ == "__main__":
    main()
