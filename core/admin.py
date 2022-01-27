from django.contrib import admin
from core.models import Eventos
# Register your models here.
class EventoAdmin(admin.ModelAdmin):
    list_display = ('id','titulo','descricao','data_evento','data_criacao', 'usuario')
    list_filter = ('titulo','descricao','data_evento','data_criacao', 'usuario')

admin.site.register(Eventos, EventoAdmin)