# Sistema de Biblioteca e Salas de Estudo

Sistema web completo para gerenciamento de empréstimos de livros, reservas de salas de estudo e painel administrativo.

## Descrição do Projeto - 

Este sistema simula o funcionamento de uma biblioteca acadêmica real, permitindo que alunos consultem livros, realizem reservas e acompanhem empréstimos. Funcionários possuem acesso a um painel administrativo completo para gerenciar livros, usuários, reservas e salas de estudo.

O projeto é dividido em frontend estático (HTML, CSS e JavaScript) e backend Django REST Framework utilizando banco SQLite.

## O sistema possui:
- Interface moderna e intuitiva
- Login via matrícula e senha
- Permissões separadas (aluno e funcionário)
- Empréstimo e devolução de livros
- Reserva de salas com status em tempo real
- Histórico de empréstimos e histórico de reservas
- Painel administrativo completo
- Scripts automáticos para criar dados de teste

## Tecnologias e Versões Utilizadas - 

### Backend:
- Python 3.11.9
- Django 5.2.8
- SQLite 3.45.1

Django CORS Headers (para permitir comunicação com o frontend)

### Frontend:
- HTML5
- CSS3
- JavaScript ES6
- Vue.js 3.x (CDN — última versão estável)

## Como Rodar o Projeto Localmente:

1. Navegue até a pasta backend
    - cd backend

2. Crie o ambiente virtual
    - python -m venv venv
    - venv\Scripts\activate

3. Instale as dependências
    - pip install django djangorestframework django-cors-headers

4. Rode as migrações
    - python manage.py migrate

5. (Opcional) Criar superusuário
    - python manage.py createsuperuser

6. Execute o servidor
    - python manage.py runserver
(assim o backend fica disponível em: http://127.0.0.1:8000)

7. Abrir o frontend
    - Basta abrir os arquivos HTML diretamente no navegador.

## Populando o Banco com Dados de Teste - 

O script dados_teste.py cria automaticamente:
- 5 usuários (3 alunos + 2 funcionários)
- 10 livros reais
- 6 salas de estudo

## Para executar o script:

1º Certifique-se de estar na pasta backend  

2º Ative o ambiente virtual  

3º Abra o shell do Django (python manage.py shell)  

4º Execute:  
 - exec(open("scripts/dados_teste.py", encoding="utf-8").read())
 - quit()

Usuários de Teste Criados Automaticamente  

## Alunos Criados Automaticamente

| Matrícula | Senha     | Nome          |
|-----------|-----------|----------------|
| 1001      | senha123  | Ana Souza      |
| 1002      | senha456  | Bruno Oliveira |
| 1003      | senha789  | Carla Pereira  |


## Funcionários Criados Automaticamente

| Matrícula | Senha     | Nome          |
|-----------|-----------|----------------|
| 2001      | func12345 | Daniel Costa   |
| 2002      | func54321 | Fernanda Lima  |

