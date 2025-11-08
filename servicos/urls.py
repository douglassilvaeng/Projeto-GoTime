from django.urls import path
from . import views

urlpatterns = [
    # ===============================
    # PÁGINA INICIAL
    # ===============================
    path('', views.index, name='index'),

    # ===============================
    # AUTENTICAÇÃO
    # ===============================
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),

    # ===============================
    # DASHBOARDS
    # ===============================
    path('cliente/dashboard/', views.dashboard_cliente, name='dashboard_cliente'),
    path('profissional/dashboard/', views.dashboard_profissional, name='dashboard_profissional'),

    # ===============================
    # AGENDAMENTO (Cliente)
    # ===============================
    path('cliente/agendar/', views.agendar_servico, name='agendar_servico'),

    # APIs para AJAX
    path('buscar_profissionais/', views.buscar_profissionais, name='buscar_profissionais'),
    path('buscar_horarios/', views.buscar_horarios_disponiveis, name='buscar_horarios'),

    # ===============================
    # HORÁRIOS (Profissional)
    # ===============================
    path('profissional/horario/novo/', views.cadastrar_horario, name='cadastrar_horario'),

    # ===============================
    # SERVIÇOS (Profissional)
    # ===============================
    path('servicos/', views.listar_servicos, name='listar_servicos'),
    path('servicos/novo/', views.criar_servico, name='criar_servico'),
    path('servicos/<int:id>/editar/', views.editar_servico, name='editar_servico'),
    path('servicos/<int:id>/excluir/', views.excluir_servico, name='excluir_servico'),
    # ===============================
    # AGENDAMENTOS (Edição / Cancelamento)
    # ===============================
    path('agendamento/<int:id>/cancelar/', views.cancelar_agendamento, name='cancelar_agendamento'),
    path('agendamento/<int:id>/editar/', views.editar_agendamento, name='editar_agendamento'),

    path('meus-dados/', views.meus_dados, name='meus_dados'),
    path('profissional/agenda/', views.agenda_profissional, name='agenda_profissional'),
    path('profissional/perfil/', views.perfil_profissional, name='perfil_profissional'),
    path('cliente/perfil/', views.perfil_cliente, name='perfil_cliente'),
    # HORÁRIOS - Ações diretas
    path('horarios/editar/<int:id>/', views.editar_horario, name='editar_horario'),
    path('horarios/excluir/<int:id>/', views.excluir_horario, name='excluir_horario'),
    path('horarios/filtro/', views.filtrar_horarios, name='filtrar_horarios'),





]
