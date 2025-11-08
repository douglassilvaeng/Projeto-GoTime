from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('servicos.urls')),  # Conecta todas as rotas do app "servicos"
]
