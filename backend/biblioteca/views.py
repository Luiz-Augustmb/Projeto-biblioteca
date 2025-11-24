from datetime import date, timedelta
from django.utils import timezone

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Livro, SalaEstudo, Emprestimo, ReservaSala, PerfilUsuario
from .serializers import (
    LivroSerializer,
    SalaEstudoSerializer,
    EmprestimoSerializer,
    ReservaSalaSerializer,
)


class LivroViewSet(viewsets.ModelViewSet):
    "Listagem e gerenciamento de livros."
    serializer_class = LivroSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Livro.objects.all().order_by('titulo')
        codigo = self.request.query_params.get('codigo')
        if codigo:
            qs = qs.filter(codigo=codigo)
        return qs


class SalaEstudoViewSet(viewsets.ReadOnlyModelViewSet):
    "Listagem de salas de estudo."
    queryset = SalaEstudo.objects.all().order_by('nome')
    serializer_class = SalaEstudoSerializer
    permission_classes = [permissions.AllowAny]


class EmprestimoViewSet(viewsets.ModelViewSet):
    "Gerenciamento de empréstimos de livros."
    serializer_class = EmprestimoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Emprestimo.objects.all().order_by('-data_emprestimo')
        usuario_id = self.request.query_params.get('usuario')
        matricula = self.request.query_params.get('matricula')
        if usuario_id:
            qs = qs.filter(usuario_id=usuario_id)
        if matricula:
            qs = qs.filter(usuario__username=matricula)
        return qs

    def create(self, request, *args, **kwargs):
        "Registra um novo empréstimo de livro."
        usuario_id = request.data.get('usuario')
        livro_id = request.data.get('livro')

        if not usuario_id or not livro_id:
            return Response({'detail': 'Usuário e livro são obrigatórios.'}, status=400)

        try:
            user = User.objects.get(id=usuario_id)
        except User.DoesNotExist:
            return Response({'detail': 'Usuário não encontrado.'}, status=404)

        try:
            livro = Livro.objects.get(id=livro_id)
        except Livro.DoesNotExist:
            return Response({'detail': 'Livro não encontrado.'}, status=404)

        if livro.quantidade_disponivel <= 0:
            return Response({'detail': 'Não há unidades disponíveis deste livro.'}, status=400)

        data_prevista = date.today() + timedelta(days=7)

        emprestimo = Emprestimo.objects.create(
            usuario=user,
            livro=livro,
            data_devolucao_prevista=data_prevista,
        )

        livro.quantidade_disponivel -= 1
        livro.save()

        serializer = self.get_serializer(emprestimo)
        return Response(serializer.data, status=201)


class ReservaSalaViewSet(viewsets.ModelViewSet):
    "reservas de salas de estudo."
    serializer_class = ReservaSalaSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = ReservaSala.objects.all().order_by('-inicio')
        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)
        return qs

    def create(self, request, *args, **kwargs):
        usuario_id = request.data.get('usuario')
        sala_id = request.data.get('sala')

        if not usuario_id or not sala_id:
            return Response({'detail': 'Usuário e sala são obrigatórios.'}, status=400)

        try:
            user = User.objects.get(id=usuario_id)
        except User.DoesNotExist:
            return Response({'detail': 'Usuário não encontrado.'}, status=404)

        try:
            sala = SalaEstudo.objects.get(id=sala_id)
        except SalaEstudo.DoesNotExist:
            return Response({'detail': 'Sala não encontrada.'}, status=404)

        agora = timezone.now()
        fim = agora + timedelta(hours=1)

        conflito = ReservaSala.objects.filter(
            sala=sala,
            status='AGENDADA',
            inicio__lt=fim,
            fim__gt=agora,
        ).exists()

        if conflito:
            return Response({'detail': 'Sala já está reservada neste horário.'}, status=400)

        reserva = ReservaSala.objects.create(
            usuario=user,
            sala=sala,
            inicio=agora,
            fim=fim,
            status='AGENDADA',
        )

        serializer = self.get_serializer(reserva)
        return Response(serializer.data, status=201)


class LoginAPIView(APIView):
    "Autentica usuário pela matrícula e senha."
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        matricula = request.data.get('matricula')
        senha = request.data.get('senha')

        if not matricula or not senha:
            return Response({'detail': 'Informe matrícula e senha.'}, status=400)

        usuario = authenticate(username=matricula, password=senha)

        if usuario is None:
            return Response({'detail': 'Matrícula ou senha inválidas.'}, status=400)

        dados = {
            'id': usuario.id,
            'matricula': usuario.username,
            'nome': usuario.get_full_name() or usuario.username,
            'is_staff': usuario.is_staff,
            'is_superuser': usuario.is_superuser,
        }
        return Response(dados)


class CriarUsuarioAPIView(APIView):
    "Cria um novo usuário (aluno ou funcionário)."
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        dados = request.data

        nome = (dados.get('nome') or '').strip()
        login = (dados.get('login') or '').strip()
        email = (dados.get('email') or '').strip()
        telefone = (dados.get('telefone') or '').strip()
        matricula = (dados.get('matricula') or '').strip()
        senha = dados.get('senha') or ''
        tipo = dados.get('tipo') or 'ALUNO'  # aluno ou funcionario

        if not nome or not matricula or not senha:
            return Response(
                {'detail': 'Nome, matrícula e senha são obrigatórios.'},
                status=400
            )

        if User.objects.filter(username=matricula).exists():
            return Response(
                {'detail': 'Já existe um usuário com essa matrícula.'},
                status=400
            )

        user = User.objects.create_user(
            username=matricula,
            password=senha,
            email=email,
            first_name=nome,
        )

        if tipo == 'FUNCIONARIO':
            user.is_staff = True
        user.save()

        perfil = PerfilUsuario.objects.create(
            usuario=user,
            matricula=matricula,
            login=login or matricula,
            telefone=telefone,
            tipo='FUNCIONARIO' if tipo == 'FUNCIONARIO' else 'ALUNO',
        )

        return Response(
            {
                'id': user.id,
                'matricula': matricula,
                'nome': nome,
                'tipo': perfil.tipo,
            },
            status=201
        )


class BuscarUsuarioAPIView(APIView):
    "Busca dados básicos de um usuário pela matrícula."
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        matricula = request.query_params.get('matricula')

        if not matricula:
            return Response({'detail': 'Informe a matrícula.'}, status=400)

        try:
            user = User.objects.get(username=matricula)
        except User.DoesNotExist:
            return Response({'detail': 'Usuário não encontrado.'}, status=404)

        dados = {
            'id': user.id,
            'matricula': user.username,
            'nome': user.get_full_name() or user.username,
            'is_staff': user.is_staff,
        }
        return Response(dados)


class StatusSalasAPIView(APIView):
    "Lista status atual das salas de estudo."
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        agora = timezone.now()
        salas = SalaEstudo.objects.all().order_by('id')

        resultado = []
        for sala in salas:
            reserva = (
                ReservaSala.objects
                .filter(
                    sala=sala,
                    status='AGENDADA',
                )
                .order_by('-inicio')
                .first()
            )
            if reserva:
                usuario = reserva.usuario
                usuario_nome = usuario.get_full_name() or usuario.username
                atrasada = reserva.fim < agora
                resultado.append({
                    'id': sala.id,
                    'nome': sala.nome,
                    'ocupada': True,
                    'usuario_nome': usuario_nome,
                    'fim': reserva.fim.isoformat(),
                    'atrasada': atrasada,
                })
            else:
                resultado.append({
                    'id': sala.id,
                    'nome': sala.nome,
                    'ocupada': False,
                    'usuario_nome': None,
                    'fim': None,
                    'atrasada': False,
                })

        return Response(resultado)


class DevolverSalaAPIView(APIView):
    "Finaliza reserva ativa de uma sala."
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        sala_id = request.data.get('sala')
        if not sala_id:
            return Response({'detail': 'Sala é obrigatória.'}, status=400)

        try:
            sala = SalaEstudo.objects.get(id=sala_id)
        except SalaEstudo.DoesNotExist:
            return Response({'detail': 'Sala não encontrada.'}, status=404)

        reserva = (
            ReservaSala.objects
            .filter(sala=sala, status='AGENDADA')
            .order_by('-inicio')
            .first()
        )

        if not reserva:
            return Response({'detail': 'Nenhuma reserva ativa para esta sala.'}, status=404)

        reserva.status = 'FINALIZADA'
        reserva.save()

        return Response({'detail': 'Sala devolvida e liberada com sucesso.'})


class EmprestimosAlunoAPIView(APIView):
    "lista todos os empréstimos ativos de um aluno:"
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        matricula = request.query_params.get('matricula')

        if not matricula:
            return Response({'detail': 'Informe a matrícula.'}, status=400)

        try:
            user = User.objects.get(username=matricula)
        except User.DoesNotExist:
            return Response({'detail': 'Aluno não encontrado.'}, status=404)

        emprestimos = Emprestimo.objects.filter(
            usuario=user,
            data_devolucao_real__isnull=True
        ).order_by('data_emprestimo')

        lista = []
        for e in emprestimos:
            lista.append({
                'id': e.id,
                'livro_titulo': e.livro.titulo,
                'livro_categoria': getattr(e.livro, 'categoria', ''),
                'data_emprestimo': e.data_emprestimo.isoformat() if e.data_emprestimo else None,
                'data_devolucao_prevista': e.data_devolucao_prevista.isoformat() if e.data_devolucao_prevista else None,
                'status': getattr(e, 'status', 'ABERTO'),
            })

        return Response({
            'aluno_id': user.id,
            'aluno_matricula': user.username,
            'aluno_nome': user.get_full_name() or user.username,
            'emprestimos': lista,
        })


class DevolverEmprestimoAPIView(APIView):
    "Registra devolução de um empréstimo:"
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        emprestimo_id = request.data.get('emprestimo_id')

        if not emprestimo_id:
            return Response({'detail': 'Empréstimo é obrigatório.'}, status=400)

        try:
            emp = Emprestimo.objects.select_related('livro').get(id=emprestimo_id)
        except Emprestimo.DoesNotExist:
            return Response({'detail': 'Empréstimo não encontrado.'}, status=404)

        if emp.data_devolucao_real:
            return Response({'detail': 'Este empréstimo já foi devolvido.'}, status=400)

        emp.data_devolucao_real = date.today()
        if hasattr(emp, 'status'):
            emp.status = 'FECHADO'
        emp.save()

        livro = emp.livro
        livro.quantidade_disponivel = (livro.quantidade_disponivel or 0) + 1
        livro.save()

        return Response({'detail': 'Devolução registrada com sucesso.'})
