from rest_framework import serializers
from .models import Livro, SalaEstudo, Emprestimo, ReservaSala


class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = '__all__'


class SalaEstudoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaEstudo
        fields = '__all__'


class EmprestimoSerializer(serializers.ModelSerializer):
    livro_titulo = serializers.CharField(source='livro.titulo', read_only=True)
    usuario_matricula = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Emprestimo
        fields = [
            'id',
            'usuario',
            'usuario_matricula',
            'livro',
            'livro_titulo',
            'data_emprestimo',
            'data_devolucao_prevista',
            'data_devolucao_real',
            'status',
        ]
        read_only_fields = ['data_emprestimo']        

class ReservaSalaSerializer(serializers.ModelSerializer):
    sala_nome = serializers.CharField(source='sala.nome', read_only=True)
    usuario_matricula = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = ReservaSala
        fields = [
            'id',
            'usuario',
            'usuario_matricula',
            'sala',
            'sala_nome',
            'inicio',
            'fim',
            'status',
        ]
        read_only_fields = ['status']
