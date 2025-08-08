# Esse código configura como o modelo Produto será exibido na interface de administração do Django (/admin).
from django.contrib import admin # Importa o módulo de administração do Django, que permite registrar e personalizar modelos no painel administrativo.

from .models import Produto # Importa o modelo Produto do arquivo models.py da mesma aplicação.

@admin.register(Produto) # Esse é um decorator que registra diretamente o modelo Produto no admin
class ProdutoAdmin(admin.ModelAdmin): # Cria uma classe de configuração para o admin do modelo Produto. Essa classe herda de admin.ModelAdmin, que permite customizar como os dados aparecem no painel de administração.
    list_display = ('nome', 'preco', 'estoque', 'slug', 'criado', 'modificado', 'ativo') # Define quais campos serão exibidos na tabela de listagem de produtos no admin.
