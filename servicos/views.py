from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Servico, Perfil, HorarioDisponivel, Agendamento
from .forms import ServicoForm, HorarioForm, AgendamentoForm


# ==============================
# PÁGINA PRINCIPAL
# ==============================
def index(request):
    # Se o usuário estiver logado, redireciona para o painel correto
    if request.user.is_authenticated:
        perfil = Perfil.objects.get(user=request.user)
        if perfil.is_profissional:
            return redirect('dashboard_profissional')
        else:
            return redirect('dashboard_cliente')

    # Caso contrário, mostra a página inicial normal
    return render(request, 'servicos/index.html')



# ==============================
# LOGIN / LOGOUT
# ==============================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                perfil = Perfil.objects.get(user=user)
                login(request, user)
                messages.success(request, f'Bem-vindo, {perfil.nome_completo}!')

                if perfil.is_profissional:
                    return redirect('dashboard_profissional')
                else:
                    return redirect('dashboard_cliente')
            except Perfil.DoesNotExist:
                messages.error(request, 'Perfil não encontrado. Contate o suporte.')
                return redirect('cadastro')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            return redirect('login')

    return render(request, 'servicos/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da conta.')
    return redirect('index')


# ==============================
# CADASTRO
# ==============================
def cadastro(request):
    if request.method == 'POST':
        nome_completo = request.POST.get('nome_completo')
        username = request.POST.get('username')
        password = request.POST.get('password')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        cpf_cnpj = request.POST.get('cpf_cnpj')
        tipo = request.POST.get('tipo')

        if User.objects.filter(username=username).exists():
            messages.error(request, '❌ Nome de usuário já cadastrado!')
            return redirect('cadastro')

        user = User.objects.create_user(username=username, password=password)
        user.save()

        perfil = Perfil.objects.create(
            user=user,
            nome_completo=nome_completo,
            telefone=telefone,
            endereco=endereco,
            cpf_cnpj=cpf_cnpj,
            is_profissional=True if tipo == 'profissional' else False
        )

        login(request, user)
        messages.success(request, f'✅ Bem-vindo, {perfil.nome_completo}! Cadastro realizado com sucesso.')

        if perfil.is_profissional:
            return redirect('dashboard_profissional')
        else:
            return redirect('dashboard_cliente')

    return render(request, 'servicos/cadastro.html')


# ==============================
# DASHBOARDS
# ==============================
# ==============================
# DASHBOARDS
# ==============================
@login_required
def dashboard_cliente(request):
    perfil = Perfil.objects.get(user=request.user)
    agendamentos = Agendamento.objects.filter(cliente=request.user).select_related(
        'servico', 'horario', 'profissional'
    )

    return render(request, 'servicos/dashboard_cliente.html', {
        'perfil': perfil,
        'agendamentos': agendamentos
    })


@login_required
def dashboard_profissional(request):
    perfil = Perfil.objects.get(user=request.user)
    servicos = Servico.objects.filter(profissional=request.user)
    horarios = HorarioDisponivel.objects.filter(profissional=request.user)
    agendamentos = Agendamento.objects.filter(profissional=request.user).select_related(
        'servico', 'cliente', 'horario'
    )

    return render(request, 'servicos/dashboard_profissional.html', {
        'perfil': perfil,
        'servicos': servicos,
        'horarios': horarios,
        'agendamentos': agendamentos
    })

@login_required
def criar_servico(request):
    perfil = Perfil.objects.get(user=request.user)

    if not perfil.is_profissional:
        messages.error(request, 'Apenas profissionais podem criar serviços.')
        return redirect('dashboard_cliente')

    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            servico = form.save(commit=False)
            servico.profissional = request.user
            servico.save()

            # 🔹 Se o modelo Perfil tiver relação ManyToMany com Servico, adiciona aqui
            if hasattr(perfil, "servicos"):
                perfil.servicos.add(servico)
                perfil.save()

            messages.success(request, '✅ Serviço criado com sucesso!')
            return redirect('listar_servicos')
    else:
        form = ServicoForm()

    return render(request, 'servicos/criar_servico.html', {'form': form})



# ==============================
# SERVIÇOS (profissional)
@login_required
def editar_servico(request, id):
    servico = get_object_or_404(Servico, id=id, profissional=request.user)
    perfil = Perfil.objects.get(user=request.user)

    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            servico = form.save()

            # 🔹 Garante que o serviço continue vinculado ao perfil do profissional
            if not perfil.servicos.filter(id=servico.id).exists():
                perfil.servicos.add(servico)

            messages.success(request, '✅ Serviço atualizado com sucesso!')
            return redirect('listar_servicos')
    else:
        form = ServicoForm(instance=servico)

    return render(request, 'servicos/editar_servico.html', {'form': form, 'servico': servico})



@login_required
def excluir_servico(request, id):
    servico = get_object_or_404(Servico, id=id, profissional=request.user)
    if request.method == 'POST':
        servico.delete()
        messages.warning(request, '🗑️ Serviço excluído com sucesso!')
        return redirect('listar_servicos')

    return render(request, 'servicos/excluir_servico.html', {'servico': servico})


# ==============================
# HORÁRIOS (profissional)
# ==============================
@login_required
def cadastrar_horario(request):
    perfil = Perfil.objects.get(user=request.user)
    if not perfil.is_profissional:
        messages.error(request, "Apenas profissionais podem cadastrar horários.")
        return redirect('dashboard_cliente')

    servicos = Servico.objects.filter(profissional=request.user)

    if request.method == 'POST':
        data = request.POST.get('data')
        servico_id = request.POST.get('servico')
        horarios = request.POST.get('horarios_selecionados', '').split(',')

        if not servico_id:
            messages.error(request, "Selecione o serviço antes de salvar os horários.")
            return redirect('cadastrar_horario')

        servico = Servico.objects.get(id=servico_id)

        if data and horarios:
            for hora in horarios:
                if hora:
                    HorarioDisponivel.objects.create(
                        profissional=request.user,
                        servico=servico,
                        data=data,
                        hora=hora,
                        disponivel=True
                    )
            messages.success(request, "✅ Horários cadastrados com sucesso!")
            return redirect('dashboard_profissional')
        else:
            messages.error(request, "Selecione uma data e pelo menos um horário.")

    horas = ["08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18"]

    return render(request, 'servicos/cadastrar_horario.html', {'horas': horas, 'servicos': servicos})






# ==============================
# AGENDAMENTO (cliente)
# ==============================
# ==============================
# AGENDAMENTO (cliente)
# ==============================
from django.http import JsonResponse

@login_required
def agendar_servico(request):
    perfil = Perfil.objects.get(user=request.user)

    if perfil.is_profissional:
        messages.error(request, "Somente clientes podem agendar serviços.")
        return redirect('dashboard_profissional')

    servicos = Servico.objects.all()
    profissionais = Perfil.objects.filter(is_profissional=True)

    if request.method == 'POST':
        servico_id = request.POST.get('servico')
        profissional_id = request.POST.get('profissional')
        data = request.POST.get('data')
        hora = request.POST.get('hora')

        if not (servico_id and profissional_id and data and hora):
            messages.error(request, "Por favor, preencha todos os campos antes de agendar.")
            return redirect('agendar_servico')

        servico = Servico.objects.get(id=servico_id)
        profissional = User.objects.get(id=profissional_id)

        # 🔹 Busca o horário disponível
        horario = HorarioDisponivel.objects.filter(
            profissional=profissional, data=data, hora=hora, disponivel=True
        ).first()

        if horario:
            # 🔹 Marca como ocupado
            horario.disponivel = False
            horario.save()

            # 🔹 Cria o registro de agendamento
            Agendamento.objects.create(
                cliente=request.user,
                profissional=profissional,
                servico=servico,
                horario=horario
            )

            messages.success(request, "✅ Agendamento confirmado com sucesso!")
            return redirect('dashboard_cliente')
        else:
            messages.error(request, "❌ Esse horário não está mais disponível. Tente outro.")

    return render(request, 'servicos/agendar_servico.html', {
        'servicos': servicos,
        'profissionais': profissionais
    })


# ==============================
# API - Buscar profissionais por serviço
# ==============================
def buscar_profissionais(request):
    servico_id = request.GET.get('servico')

    if not servico_id:
        return JsonResponse({'profissionais': []})

    # Busca profissionais que oferecem o serviço selecionado
    profissionais = Perfil.objects.filter(
        is_profissional=True,
        servicos__id=servico_id
    ).select_related('user')

    data = [
        {
            'id': p.user.id,  # <<< corrigido: usar p.user.id (User vinculado)
            'nome': p.nome_completo or p.user.username
        }
        for p in profissionais
    ]
    return JsonResponse({'profissionais': data})



# ==============================
# API - Buscar horários disponíveis
# ==============================
@login_required
def buscar_horarios_disponiveis(request):
    profissional_id = request.GET.get('profissional')
    data = request.GET.get('data')

    if not (profissional_id and data):
        return JsonResponse({'horarios': []})

    horarios = HorarioDisponivel.objects.filter(
        profissional_id=profissional_id,
        data=data,
        disponivel=True
    ).values_list('hora', flat=True)

    return JsonResponse({'horarios': list(horarios)})

@login_required
def listar_servicos(request):
    servicos = Servico.objects.filter(profissional=request.user)
    return render(request, 'servicos/listar_servicos.html', {'servicos': servicos})

@login_required
def cancelar_agendamento(request, id):
    agendamento = get_object_or_404(Agendamento, id=id)

    # 🔐 Verificação de permissão
    if request.user != agendamento.cliente and request.user != agendamento.profissional:
        messages.error(request, "Você não tem permissão para cancelar este agendamento.")
        return redirect('dashboard_cliente')

    if request.method == 'POST':
        # 🔄 Libera o horário novamente
        agendamento.horario.disponivel = True
        agendamento.horario.save()

        agendamento.delete()
        messages.warning(request, "❌ Agendamento cancelado com sucesso.")
        return redirect('dashboard_profissional' if agendamento.profissional == request.user else 'dashboard_cliente')

    return render(request, 'servicos/cancelar_agendamento.html', {'agendamento': agendamento})

@login_required
def editar_agendamento(request, id):
    agendamento = get_object_or_404(Agendamento, id=id, profissional=request.user)

    if request.method == 'POST':
        novo_data = request.POST.get('data')
        novo_hora = request.POST.get('hora')

        if novo_data and novo_hora:
            # 🔄 Libera o horário antigo
            agendamento.horario.disponivel = True
            agendamento.horario.save()

            # 🔎 Busca um novo horário disponível
            novo_horario = HorarioDisponivel.objects.filter(
                profissional=request.user,
                data=novo_data,
                hora=novo_hora,
                disponivel=True
            ).first()

            if not novo_horario:
                messages.error(request, "❌ Horário indisponível.")
                return redirect('dashboard_profissional')

            # 🔁 Atualiza o agendamento
            agendamento.horario = novo_horario
            agendamento.horario.disponivel = False
            agendamento.horario.save()
            agendamento.save()

            messages.success(request, "✅ Agendamento atualizado com sucesso.")
            return redirect('dashboard_profissional')

    horarios = HorarioDisponivel.objects.filter(
        profissional=request.user,
        disponivel=True
    )

    return render(request, 'servicos/editar_agendamento.html', {
        'agendamento': agendamento,
        'horarios': horarios
    })

@login_required
def meus_dados(request):
    perfil = Perfil.objects.get(user=request.user)

    if request.method == 'POST':
        perfil.nome_completo = request.POST.get('nome_completo')
        perfil.telefone = request.POST.get('telefone')
        perfil.endereco = request.POST.get('endereco')
        perfil.save()

        user = request.user
        nova_senha = request.POST.get('nova_senha')
        if nova_senha:
            user.set_password(nova_senha)
            user.save()

        messages.success(request, "✅ Dados atualizados com sucesso!")
        return redirect('meus_dados')

    return render(request, 'servicos/meus_dados.html', {'perfil': perfil})

@login_required
def dashboard_profissional(request):
    perfil = Perfil.objects.get(user=request.user)
    servicos = Servico.objects.filter(profissional=request.user)
    horarios_disponiveis = HorarioDisponivel.objects.filter(
        profissional=request.user, disponivel=True
    ).order_by('data', 'hora')
    agendamentos = Agendamento.objects.filter(
        profissional=request.user
    ).select_related('servico', 'cliente', 'horario').order_by('horario__data', 'horario__hora')

    return render(request, 'servicos/dashboard_profissional.html', {
        'perfil': perfil,
        'servicos': servicos,
        'horarios_disponiveis': horarios_disponiveis,
        'agendamentos': agendamentos
    })

@login_required
def agenda_profissional(request):
    perfil = Perfil.objects.get(user=request.user)

    if not perfil.is_profissional:
        messages.error(request, "Apenas profissionais têm acesso a essa página.")
        return redirect('dashboard_cliente')

    # 🔹 Filtro por período (usado pelo formulário de datas)
    data_inicio = request.GET.get('inicio')
    data_fim = request.GET.get('fim')

    agendamentos = Agendamento.objects.filter(
        profissional=request.user
    ).select_related('horario', 'cliente', 'servico').order_by('horario__data', 'horario__hora')

    horarios_disponiveis = HorarioDisponivel.objects.filter(
        profissional=request.user,  # <-- 🔹 filtro essencial
        disponivel=True
    ).order_by('data', 'hora')

    # 🔹 Filtro por data opcional (formulário de período)
    if data_inicio and data_fim:
        horarios_disponiveis = horarios_disponiveis.filter(data__range=[data_inicio, data_fim])

    return render(request, 'servicos/agenda_profissional.html', {
        'perfil': perfil,
        'agendamentos': agendamentos,
        'horarios_disponiveis': horarios_disponiveis,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    })


@login_required
def perfil_profissional(request):
    perfil = Perfil.objects.get(user=request.user)

    if not perfil.is_profissional:
        messages.error(request, "Somente profissionais podem acessar esta página.")
        return redirect('dashboard_cliente')

    if request.method == 'POST':
        perfil.nome_completo = request.POST.get('nome_completo')
        perfil.telefone = request.POST.get('telefone')
        perfil.endereco = request.POST.get('endereco')
        perfil.cpf_cnpj = request.POST.get('cpf_cnpj')
        perfil.save()
        messages.success(request, "✅ Dados atualizados com sucesso!")
        return redirect('perfil_profissional')

    return render(request, 'servicos/perfil_profissional.html', {'perfil': perfil})

@login_required
def perfil_cliente(request):
    perfil = Perfil.objects.get(user=request.user)

    if perfil.is_profissional:
        messages.error(request, "Apenas clientes acessam esta página.")
        return redirect('dashboard_profissional')

    if request.method == 'POST':
        perfil.nome_completo = request.POST.get('nome_completo')
        perfil.telefone = request.POST.get('telefone')
        perfil.endereco = request.POST.get('endereco')
        perfil.cpf_cnpj = request.POST.get('cpf_cnpj')
        perfil.save()
        messages.success(request, "✅ Seus dados foram atualizados com sucesso!")
        return redirect('perfil_cliente')

    return render(request, 'servicos/perfil_cliente.html', {'perfil': perfil})

@login_required
def editar_horario(request, id):
    horario = get_object_or_404(HorarioDisponivel, id=id, profissional=request.user)

    if request.method == 'POST':
        nova_data = request.POST.get('data')
        nova_hora = request.POST.get('hora')

        if nova_data and nova_hora:
            horario.data = nova_data
            horario.hora = nova_hora
            horario.save()
            messages.success(request, "✅ Horário atualizado com sucesso!")
            return redirect('agenda_profissional')
        else:
            messages.error(request, "❌ Preencha todos os campos corretamente.")

    return render(request, 'servicos/editar_horario.html', {'horario': horario})

@login_required
def excluir_horario(request, id):
    horario = get_object_or_404(HorarioDisponivel, id=id, profissional=request.user)

    if request.method == 'POST':
        horario.delete()
        messages.warning(request, "🗑️ Horário excluído com sucesso!")
        return redirect('agenda_profissional')

    return render(request, 'servicos/excluir_horario.html', {'horario': horario})

from django.utils.dateparse import parse_date

@login_required
def filtrar_horarios(request):
    perfil = Perfil.objects.get(user=request.user)

    if not perfil.is_profissional:
        messages.error(request, "Apenas profissionais podem filtrar horários.")
        return redirect('dashboard_cliente')

    data_inicio = request.GET.get('inicio')
    data_fim = request.GET.get('fim')

    horarios_filtrados = HorarioDisponivel.objects.filter(
        profissional=request.user,
        disponivel=True
    )

    if data_inicio:
        horarios_filtrados = horarios_filtrados.filter(data__gte=parse_date(data_inicio))
    if data_fim:
        horarios_filtrados = horarios_filtrados.filter(data__lte=parse_date(data_fim))

    agendamentos = Agendamento.objects.filter(profissional=request.user)

    return render(request, 'servicos/agenda_profissional.html', {
        'perfil': perfil,
        'agendamentos': agendamentos,
        'horarios_disponiveis': horarios_filtrados,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    })


