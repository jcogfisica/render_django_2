"""
Django settings para o projeto Django2.

Este arquivo é gerado automaticamente pelo comando 'django-admin startproject' na versão Django 5.2.5.

Para mais informações sobre configurações do Django, consulte:
https://docs.djangoproject.com/en/5.2/topics/settings/

Para a lista completa de configurações e seus valores, consulte:
https://docs.djangoproject.com/en/5.2/ref/settings/
"""
# Importações necessárias para manipulação de caminhos e variáveis de ambiente

import os
# Biblioteca padrão do Python que fornece funcionalidades para interagir com o sistema operacional.
# Aqui é usada principalmente para manipulação de variáveis de ambiente, criação e junção de caminhos de arquivos,
# verificação de existência de arquivos, entre outros.

from pathlib import Path
# Módulo da biblioteca padrão do Python que facilita a manipulação de caminhos de forma orientada a objetos
# e independente do sistema operacional (Windows, Linux, etc).
# Permite, por exemplo, construir caminhos absolutos relativos ao arquivo atual com métodos mais intuitivos que 'os.path'.

import dj_database_url
# Biblioteca externa utilizada para interpretar URLs de conexão de banco de dados em um dicionário de configuração
# que o Django aceita diretamente.
# Facilita a configuração do banco de dados a partir de variáveis de ambiente (como DATABASE_URL),
# especialmente útil em ambientes de produção e deploys automatizados.

from google.oauth2 import service_account
# Importa a classe 'service_account' do pacote google.oauth2.
# Essa classe é usada para carregar credenciais de contas de serviço Google a partir de arquivos JSON,
# permitindo autenticação automatizada com APIs Google, neste caso, para uso do Google Cloud Storage.

import tempfile
# Biblioteca padrão do Python para criação e manipulação de arquivos e diretórios temporários,
# usados aqui para armazenar temporariamente as credenciais do Google Cloud carregadas via variável de ambiente JSON,
# garantindo que a API do GCS receba um arquivo físico, já que ela não aceita uma string diretamente.

# Configuração do banco de dados principal da aplicação Django usando a biblioteca dj_database_url:
DATABASES = {
    'default': dj_database_url.config(
        default = 'mysql://jcog:MON010deo010@localhost:3306/Django2',
        # Caso a variável de ambiente DATABASE_URL não esteja definida,
        # usa a URL padrão do banco MySQL local especificada acima.

        conn_max_age = 600,
        # Tempo máximo (em segundos) que a conexão com o banco pode permanecer aberta e reutilizada.
        # Usado para melhorar a performance evitando abrir uma conexão a cada requisição.

        ssl_require = False
        # Define se a conexão com o banco de dados requer SSL.
        # False significa que a conexão não usará criptografia SSL.
    )
}

# Construção do caminho absoluto para a raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR será um objeto Path que representa o diretório dois níveis acima deste arquivo settings.py,
# ou seja, o diretório raiz do projeto Django2.

SECRET_KEY = 'django-insecure-@(3(^n#fjqx1$3+ji)zm-mhgu1edap!y6crwhho_8n0q36uy7u'
# Chave secreta usada internamente pelo Django para funções de segurança, como criptografia de sessões e tokens CSRF.
# Nunca deve ser exposta publicamente, pois comprometeria a segurança do site.

RENDER = os.environ.get('RENDER') == 'TRUE'
# Variável de ambiente usada pelo serviço Render para identificar se está em ambiente de produção.
# Retorna True se RENDER estiver definida como 'TRUE', caso contrário False.

DEBUG = not RENDER
# DEBUG será True somente quando não estiver no ambiente Render.
# Isso ativa/desativa o modo de depuração do Django.

ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Permite acesso local
# Lista de hosts permitidos para responder requisições HTTP.
# Usar '*' permite acesso irrestrito de qualquer domínio, o que é seguro somente para desenvolvimento.

if not DEBUG:
    # Obtém o hostname externo definido automaticamente pelo serviço Render
    # Essa variável de ambiente contém o domínio pelo qual seu app é acessado publicamente,
    # por exemplo: 'mysite-nurz.onrender.com'
    external = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

    if external:
        ALLOWED_HOSTS.append(external)
        # Adiciona o hostname externo à lista ALLOWED_HOSTS para permitir requisições HTTP vindas desse domínio.
        # Sem essa configuração, o Django bloquearia requisições com erro 400 (Bad Host Header).

    ALLOWED_HOSTS.append('.onrender.com')
    # Adiciona um domínio genérico para permitir qualquer subdomínio do domínio 'onrender.com'.
    # Ao usar o prefixo '.' (ponto) antes do domínio, Django aceita o domínio principal
    # e todos os seus subdomínios, por exemplo:
    # 'onrender.com', 'www.onrender.com', 'mysite.onrender.com', etc.
    # Isso é importante para garantir que seu app funcione mesmo que o subdomínio mude ou
    # você crie subdomínios adicionais.

INSTALLED_APPS = [
    'django.contrib.admin',         # Interface administrativa padrão do Django.
    'django.contrib.auth',          # Sistema de autenticação (login, permissões).
    'django.contrib.contenttypes',  # Suporte para tipos genéricos de conteúdo.
    'django.contrib.sessions',      # Gerenciamento de sessões entre requisições.
    'django.contrib.messages',      # Framework para mensagens temporárias ao usuário.
    'django.contrib.staticfiles',   # Gerenciamento e coleta de arquivos estáticos (CSS, JS, imagens).
    'core',                        # Aplicação customizada criada para o projeto.
    'bootstrap4',                  # Integração com o framework CSS Bootstrap 4 para frontend.
    'stdimage',                    # Biblioteca para manipulação avançada de imagens no Django.
    'pictures',                    # Biblioteca para galerias e manipulação de imagens.
    'storages'                    # Biblioteca para integração com armazenamento em nuvem (Google Cloud Storage).
]
# Lista de aplicações Django e apps externos que estão ativados neste projeto.
# Cada string é o caminho do módulo do app, que será carregado automaticamente pelo Django.

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',               # Aplica medidas básicas de segurança.
    'whitenoise.middleware.WhiteNoiseMiddleware',                  # Serve arquivos estáticos no ambiente de produção.
    'django.contrib.sessions.middleware.SessionMiddleware',        # Gerencia o ciclo de vida da sessão HTTP.
    'django.middleware.common.CommonMiddleware',                   # Middleware para tarefas comuns (como redirecionamento).
    'django.middleware.csrf.CsrfViewMiddleware',                   # Proteção contra ataques CSRF.
    'django.contrib.auth.middleware.AuthenticationMiddleware',     # Garante autenticação do usuário em requisições.
    'django.contrib.messages.middleware.MessageMiddleware',        # Processa mensagens para o sistema de mensagens do Django.
    'django.middleware.clickjacking.XFrameOptionsMiddleware',      # Protege contra ataques de clickjacking.
]
# Configuração dos middlewares - componentes que processam a requisição/resposta.
# Eles atuam antes das views e depois para tarefas como segurança, sessão e mensagens.

ROOT_URLCONF = 'Django2.urls'
# Indica o módulo de configuração principal das URLs do projeto.

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Motor padrão de templates do Django.
        'DIRS': ['templates'],  # Diretórios externos onde o Django também procurará templates.
        'APP_DIRS': True,       # Permite carregar templates localizados na pasta 'templates' de cada app instalado.
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',      # Adiciona o objeto HttpRequest aos templates.
                'django.contrib.auth.context_processors.auth',      # Adiciona o contexto de autenticação (usuário logado, etc).
                'django.contrib.messages.context_processors.messages' # Adiciona o contexto de mensagens flash.
            ],
        },
    },
]
# Configuração do sistema de templates do Django (arquivos HTML dinâmicos).
# Context processors injetam variáveis globais em todos os templates, facilitando uso em layouts.

PICTURES = {
    "BREAKPOINTS": {'thumb': 200, "mobile": 576, "tablet": 768, "desktop": 992},
    "GRID_COLUMNS": 12,
    "CONTAINER_WIDTH": 1200,
    "FILE_TYPES": ["WEBP", "JPG", "JPEG", "BMP", "PNG"],
    "PIXEL_DENSITIES": [1, 2],
    "USE_PLACEHOLDERS": True,
}
# Configurações específicas para a biblioteca 'pictures' (galeria/imagens).
# Define tamanhos responsivos, tipos aceitos e uso de placeholders para carregamento progressivo.

WSGI_APPLICATION = 'Django2.wsgi.application'
# Definição da aplicação WSGI (interface entre o Django e o servidor web).

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},  # Previne senhas similares a atributos do usuário.
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},            # Exige comprimento mínimo da senha.
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},           # Previne uso de senhas comuns.
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},          # Previne senhas somente numéricas.
]
# Validadores de senha para autenticação, garantindo segurança mínima nas senhas criadas pelos usuários.

LANGUAGE_CODE = 'pt-br'
# Define o idioma padrão da aplicação como Português do Brasil.

TIME_ZONE = 'America/Sao_Paulo'
# Define o fuso horário padrão.

USE_I18N = True
# Habilita suporte a tradução e internacionalização.

USE_TZ = True
# Ativa suporte a objetos datetime com informação de fuso horário.

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Define o tipo padrão de campo para chaves primárias automáticas.

# -------------------------------------------------------------------
# Configuração para autenticação e acesso ao Google Cloud Storage (GCS)
# -------------------------------------------------------------------

path_credenciais = None
# path_credenciais é o caminho para o arquivo de credenciais JSON, o qual contém as credenciais para acessar o bucket do Google Cloud

filename = "credenciais.json"
# Nome do arquivo de credenciais

GS_CREDENTIALS = None
# Objeto contendo as credenciais propriamente ditas

if not DEBUG:
    # Se a aplicação estiver em produção

    path_credenciais = "/etc/secrets/" + filename
    # Caminho para o arquivo de credenciais no ambiente do Render

    if os.path.exists(path_credenciais): # se o caminho path_credenciais aponta para o arquivo cujo nome é filename
        # print(f"O arquivo {path_credenciais} existe!")

        GS_CREDENTIALS = service_account.Credentials.from_service_account_file(path_credenciais)
        # Carrega as credenciais do arquivo JSON utilizando a classe service_account.
        # O metodo from_service_account_file lê o arquivo JSON e retorna um objeto credencial: GS_CREDENTIALS

    else:
        raise Exception(f"O arquivo {path_credenciais} não existe!")
        # Retorna uma exceção mostrando que path_credenciais não aponta para o arquivo JSON


else:
    path_credenciais = os.path.join(BASE_DIR, filename)
    # Caminho para o arquivo de credenciais no ambiente local

    if os.path.exists(path_credenciais): # se o caminho path_credenciais aponta para o arquivo cujo nome é filename
        # print(f"O arquivo {path_credenciais} existe!")

        GS_CREDENTIALS = service_account.Credentials.from_service_account_file(path_credenciais)
        # Carrega as credenciais do arquivo JSON utilizando a classe service_account.
        # O metodo from_service_account_file lê o arquivo JSON e retorna um objeto credencial: GS_CREDENTIALS

    else:
        raise Exception(f"O arquivo {path_credenciais} não existe!")
        # Retorna uma exceção mostrando que path_credenciais não aponta para o arquivo JSON

# -------------------------------------------------------------------
# Configurações do Google Cloud Storage para arquivos estáticos e mídia
# -------------------------------------------------------------------

GS_BUCKET_NAME = "django-render"
# Nome do bucket no Google Cloud Storage onde os arquivos serão armazenados.

# ---------- INÍCIO DA CONFIGURAÇÃO CONDICIONAL PARA AMBIENTES ----------

# Abaixo implementamos uma diferenciação entre o ambiente de produção (quando DEBUG = False)
# e o ambiente de desenvolvimento local (DEBUG = True), para que localmente os arquivos estáticos e de mídia
# sejam armazenados e servidos pelo sistema de arquivos local, facilitando o desenvolvimento e testes.
# Já em produção, os arquivos serão armazenados e servidos pelo bucket do Google Cloud Storage (GCS).
#
# Isso resolve o problema onde, localmente, a aplicação tentava enviar arquivos estáticos diretamente para o GCS,
# o que pode não ser desejável ou configurado para funcionar no ambiente local.
#
# Essa abordagem permite que:
# - No desenvolvimento local, arquivos estáticos e mídia sejam facilmente acessados e modificados localmente.
# - Na produção, o uso do armazenamento em nuvem garante alta disponibilidade e escalabilidade.

if not DEBUG:
    STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"
    MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
    # URLs públicas para acesso direto a arquivos estáticos e de mídia hospedados no bucket GCS.

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "bucket_name": GS_BUCKET_NAME,
                "credentials": GS_CREDENTIALS,
                "location": "media",
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "bucket_name": GS_BUCKET_NAME,
                "credentials": GS_CREDENTIALS,
                "location": "static",
            },
        },
    }
    # Configuração que o Django usa para definir como e onde ele vai armazenar arquivos — principalmente arquivos estáticos (CSS, JS, imagens do layout)
    # e arquivos de mídia (imagens, documentos enviados pelo usuário).
    # Quando você usa armazenamento em nuvem — aqui, o Google Cloud Storage (GCS) — o Django precisa saber:
    # 1) Qual é o backend de armazenamento (no caso, o storages.backends.gcloud.GoogleCloudStorage, que é a integração do Django com o Google Cloud Storage)
    # 2) Em qual bucket os arquivos vão ser guardados (bucket_name)
    # 3) Quais credenciais usar para autenticar e ter permissão de acessar esse bucket (credentials)
    # 4) E uma "pasta" (localização) dentro do bucket para organizar os arquivos (location), por exemplo "media" para arquivos de mídia e "static" para arquivos estáticos
    # O que significa cada chave?
    # "default": define o armazenamento padrão para arquivos de mídia enviados pelo usuário (exemplo: fotos enviadas, PDFs etc)
    # "staticfiles" — define o armazenamento para arquivos estáticos do seu site (exemplo: CSS, JavaScript, imagens do tema)
    # Cada um aponta para o mesmo bucket, mas em locais diferentes (location: "media" e location: "static"),
    # assim os arquivos ficam organizados separadamente dentro do bucket.

    # Configuração para produção no GCS:
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    # É uma configuração do Django que define qual backend de armazenamento será usado para arquivos de mídia
    # (ou seja, arquivos enviados por usuários, como fotos, documentos, etc).
    # 'storages.backends.gcloud.GoogleCloudStorage' é o backend do pacote django-storages para armazenar arquivos no Google Cloud Storage (GCS).
    # Quando o Django salva um arquivo de mídia (por exemplo, um upload de imagem),
    # ele usará esse backend para enviar o arquivo para o bucket configurado no GCS, ao invés de salvar localmente no disco do servidor.

    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    # Define qual backend será usado para armazenar e servir os arquivos estáticos (CSS, JavaScript, imagens fixas usadas pelo site).
    # Também aponta para o backend do GCS. Isso indica que, quando você executar o comando collectstatic do Django,
    # os arquivos estáticos serão enviados para o bucket no Google Cloud, ao invés de serem guardados localmente.

else:
    STATIC_URL = '/static/'
    # Define a URL base para acessar os arquivos estáticos localmente, ou seja, quando você estiver desenvolvendo ou rodando o projeto em modo debug (não em produção).

    MEDIA_URL = '/media/'
    # Define a URL base para acessar arquivos de mídia (uploads de usuários) localmente.

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Diretório local no servidor onde o comando collectstatic vai reunir todos os arquivos estáticos do projeto.
    # Em ambiente local, o Django coleta todos os arquivos estáticos (de apps e pastas STATICFILES_DIRS) e os coloca nessa pasta para serem servidos pelo servidor local.

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    # Diretório local onde o Django salva os arquivos de mídia (uploads de usuários) quando você está rodando o projeto localmente.
    # Para desenvolvimento local, onde normalmente não se usa armazenamento em nuvem, mas salva arquivos no disco do próprio computador.

    # Pode adicionar diretórios extras para arquivos estáticos, caso use:
    # STATICFILES_DIRS = [
        #BASE_DIR / 'core' / 'static',
    #]

    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    # Define o backend de armazenamento para arquivos de mídia (uploads feitos por usuários) usando o sistema de arquivos local.
    # Ao invés de enviar para o Google Cloud Storage, o Django vai salvar os arquivos no diretório local definido por MEDIA_ROOT.
    # Esse é o comportamento padrão do Django quando você não configura nada relacionado a armazenamento em nuvem.

    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    # Backend padrão para lidar com arquivos estáticos (CSS, JS, imagens do site).
    # Ao rodar python manage.py collectstatic, todos os arquivos estáticos serão reunidos no diretório local STATIC_ROOT.    #
    # Eles não serão enviados para um bucket em nuvem.
    # Esse backend apenas cuida de copiar e organizar os arquivos localmente para que o servidor de desenvolvimento ou um servidor web (como Nginx) possa servi-los.

# ---------- FIM DA CONFIGURAÇÃO CONDICIONAL PARA AMBIENTES ----------

# Comentários adicionais:
# Ao executar o comando 'python manage.py collectstatic', o Django irá coletar
# os arquivos estáticos de todos os apps instalados e também de STATICFILES_DIRS
# e armazená-los em STATIC_ROOT para posteriormente fazer upload no bucket.

"""
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = '<PASSWORD>'
EMAIL_HOST_USER = 'no-reply@seudominio.com'
"""
# Configurações de email, atualmente comentadas.
# Servem para enviar emails via servidor SMTP, como confirmação de cadastro, reset de senha, etc.
