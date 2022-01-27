from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from core.models import Eventos
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.http.response import HttpResponseNotFound, HttpResponseNotAllowed, Http404, JsonResponse

# Create your views here.
def hello(request, nome, idade):
    return HttpResponse('<h1>Hello World {} de {} anos</h1>'.format(nome, idade))

def index(request):
    return redirect('/agenda/')

def evento(request, titulo_evento):
    eve = Eventos.objects.get(titulo=titulo_evento)
    return HttpResponse('<h1>Evento {} </h1>'.format(eve.descricao))

def login_user(request):
    return render(request, 'login.html')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        senha = request.POST.get('password')
        usuario = authenticate(username=username, password=senha)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, 'Usuário ou senha inválido')
    else:
        redirect('/')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def lista_eventos(request):
    # eve = Eventos.objects.get(id=1)
    usuario = request.user
    data_atual = datetime.now()
    if usuario is not None:
        #eventos = Eventos.objects.filter(usuario=usuario, data_evento__gt=data_atual)
        eventos = Eventos.objects.filter(usuario=usuario)
    else:
        eventos = Eventos.objects.all()

    dados = {'eventos': eventos }
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def cadevento(request):
    id_evento = request.GET.get('id')
    print(id_evento)
    dados = {}
    if id_evento:
        dados['eventos'] = Eventos.objects.get(id=id_evento)
    return render(request, 'cadevento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        local = request.POST.get('local')
        data_evento = request.POST.get('data_evento')
        id_evento = request.POST.get('id_evento')

        if id_evento:
            eve = Eventos.objects.get(id=id_evento)
            if eve.usuario == request.user:
                eve.titulo=titulo
                eve.local = local
                eve.descricao = descricao
                eve.data_evento = data_evento
                eve.save()

            #Forma opcinal de fazer update
            '''eve = Eventos.objects.filter(id=id_evento).update(titulo=titulo,
                                     descricao=descricao,
                                     local=local,
                                     data_evento=data_evento)'''
        else:
            eve = Eventos.objects.create(titulo=titulo,
                                     descricao=descricao,
                                     local=local,
                                     data_evento=data_evento,
                                     usuario=request.user)

        if eve is not None:
            return redirect('/')
        else:
            messages.error(request, 'Preencha todos campos')
    else:
        redirect('/')
    return render(request, 'login.html')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    # Exclusão direta sem validação...
    # Eventos.objects.filter(id=id_evento).delete()
    try:
        eve = Eventos.objects.get(id=id_evento)

        if eve is None:
            return HttpResponseNotFound
        else:
            if eve.usuario == request.user:
                eve.delete()
            else:
                HttpResponseNotAllowed
        return redirect('/')
    except Exception:
        raise Http404()

def json_lista(request, id_usuario):
    print(id_usuario)

    try:
        usuario = User.objects.get(id=id_usuario)
        eventos = Eventos.objects.filter(usuario=usuario).values('id', 'titulo', 'descricao')
    except User.DoesNotExist:
        eventos = Eventos.objects.all().values('id', 'titulo')

    return JsonResponse(list(eventos), safe=False)






