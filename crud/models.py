# crud/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Evento(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateTimeField()
    local = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Mensagem(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='mensagens')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_envio = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Mensagem de {self.autor.username} em {self.evento.nome}'
