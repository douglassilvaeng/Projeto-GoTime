from django.shortcuts import render

def index(request):
    return render(request, 'template/index.html')

def login_view(request):
    return render(request, 'template/login.html')

def cadastro(request):
    return render(request, 'template/cadastro.html')

def dashboard_cliente(request):
    return render(request, 'template/dashboard_cliente.html')

def dashboard_profissional(request):
    return render(request, 'template/dashboard_profissional.html')

def agendamento(request):
    return render(request, 'template/agendamento.html')
