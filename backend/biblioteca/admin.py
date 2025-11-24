from django.contrib import admin
from .models import Livro, SalaEstudo, Emprestimo, ReservaSala, PerfilUsuario


admin.site.register(Livro)
admin.site.register(SalaEstudo)
admin.site.register(Emprestimo)
admin.site.register(ReservaSala)
admin.site.register(PerfilUsuario)
