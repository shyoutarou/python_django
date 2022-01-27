from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Eventos(models.Model):
    titulo = models.CharField(max_length=100,verbose_name='Título')
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(verbose_name='Data Evento')
    local = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now=True, verbose_name='Data Criação')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'evento'

    def __str__(self):
        return self.titulo

    def data_evento_format(self):
        return self.data_evento.strftime('%d/%m/%Y %H:%M')

    def get_eventos_atrasados(self):
        if self.data_evento < datetime.now():
            return True
        else:
            return False
