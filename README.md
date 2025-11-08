# 💈 GoTime

Sistema de agendamento e gestão de serviços unissex desenvolvido em **Django (Python)**.  
O GoTime conecta **clientes e profissionais** de beleza, estética e bem-estar, permitindo agendamento online, controle de horários e gerenciamento de serviços de forma simples e moderna.

---

## 🚀 Funcionalidades Principais
- Cadastro de **clientes e profissionais**
- Painel separado para cada tipo de usuário
- **Agendamento online** com confirmação e cancelamento
- **Edição e exclusão de horários**
- **Filtro de datas** para visualizar compromissos
- Interface moderna, responsiva e intuitiva

---

## 🛠️ Tecnologias Utilizadas
- **Python 3.11+**
- **Django 5+**
- **HTML5 / CSS3 / Bootstrap 5**
- **SQLite** (banco de dados padrão)
- **JavaScript** (interatividade no front-end)

---

## 📦 Instalação do Projeto

```bash
# Clone o repositório
git clone https://github.com/douglassilvaeng/Projeto-GoTime.git
cd Projeto-GoTime

# Crie um ambiente virtual
python -m venv .venv

# Ative o ambiente
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate

# Inicie o servidor
python manage.py runserver 0.0.0.0:8080
