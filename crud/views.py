from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_POST
from rest_framework.authtoken.models import Token
from .models import Evento, Mensagem
from .forms import EventoForm  # Importando EventoForm do arquivo forms.py
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, api_view


@login_required
def index(request):
    return HttpResponse("Hello, world. You're at the CRUD index.")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redireciona para a página inicial após o registro
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'crud/lista_eventos.html', {'eventos': eventos})

def cria_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_eventos')
    else:
        form = EventoForm()
    return render(request, 'crud/cria_evento.html', {'form': form})

def atualiza_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('lista_eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'crud/atualiza_evento.html', {'form': form})

def deleta_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'POST':
        evento.delete()
        return redirect('lista_eventos')
    return render(request, 'crud/deleta_evento.html', {'evento': evento})



@login_required
def chat_view(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    mensagens = Mensagem.objects.filter(evento=evento)
    return render(request, 'chat_fastapi/templates/chat.html', {'evento': evento, 'mensagens': mensagens})

@csrf_protect
def login_view(request):
    return render(request, 'chat_fastapi/templates/login.html')

@csrf_exempt
@require_POST
def obtain_token(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({'access_token': token.key})
    else:
        return JsonResponse({'error': 'Credenciais inválidas'}, status=400)
    
@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def validate_token(request):
    if request.user.is_authenticated:
        return JsonResponse({'valid': True})
    else:
        return JsonResponse({'valid': False}, status=401)