from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LivroViewSet,
    SalaEstudoViewSet,
    EmprestimoViewSet,
    ReservaSalaViewSet,
    LoginAPIView,
    CriarUsuarioAPIView,
    BuscarUsuarioAPIView,
    StatusSalasAPIView,
    DevolverSalaAPIView,
    EmprestimosAlunoAPIView,
    DevolverEmprestimoAPIView,
)

router = DefaultRouter()
router.register(r'livros', LivroViewSet, basename='livros')
router.register(r'salas-estudo', SalaEstudoViewSet, basename='salas-estudo')
router.register(r'emprestimos', EmprestimoViewSet, basename='emprestimos')
router.register(r'reservas-salas', ReservaSalaViewSet, basename='reservas-salas')

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('usuarios/', CriarUsuarioAPIView.as_view(), name='criar-usuario'),
    path('buscar-usuario/', BuscarUsuarioAPIView.as_view(), name='buscar-usuario'),
    path('status-salas/', StatusSalasAPIView.as_view(), name='status-salas'),
    path('devolver-sala/', DevolverSalaAPIView.as_view(), name='devolver-sala'),
    path('emprestimos-aluno/', EmprestimosAlunoAPIView.as_view(), name='emprestimos-aluno'),
    path('devolver-emprestimo/', DevolverEmprestimoAPIView.as_view(), name='devolver-emprestimo'),

    path('', include(router.urls)),
]
