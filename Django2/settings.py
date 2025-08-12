"""
Django settings para o projeto Django2.

Este arquivo é gerado automaticamente pelo comando 'django-admin startproject' na versão Django 5.2.5.

Para mais informações sobre configurações do Django, consulte:
https://docs.djangoproject.com/en/5.2/topics/settings/

Para a lista completa de configurações e seus valores, consulte:
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import sys

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
        default='mysql://jcog:MON010deo010@localhost:3306/Django2',
        # Caso a variável de ambiente DATABASE_URL não esteja definida,
        # usa a URL padrão do banco MySQL local especificada acima.

        conn_max_age=600,
        # Tempo máximo (em segundos) que a conexão com o banco pode permanecer aberta e reutilizada.
        # Usado para melhorar a performance evitando abrir uma conexão a cada requisição.

        ssl_require=False
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
        # Adiciona o hostname externo à lista ALLOWED_HOSTS para permitir requisições HTTP vindas desse domínio.
        # Sem essa configuração, o Django bloquearia requisições com erro 400 (Bad Host Header).
        ALLOWED_HOSTS.append(external)

    # Adiciona um domínio genérico para permitir qualquer subdomínio do domínio 'onrender.com'.
    # Ao usar o prefixo '.' (ponto) antes do domínio, Django aceita o domínio principal
    # e todos os seus subdomínios, por exemplo:
    # 'onrender.com', 'www.onrender.com', 'mysite.onrender.com', etc.
    # Isso é importante para garantir que seu app funcione mesmo que o subdomínio mude ou
    # você crie subdomínios adicionais.
    ALLOWED_HOSTS.append('.onrender.com')

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

gcp_credentials_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
# A variável de ambiente 'GOOGLE_APPLICATION_CREDENTIALS_JSON' deve conter o conteúdo completo
# do arquivo JSON da conta de serviço (service account) do Google Cloud em formato texto.
# Esta abordagem elimina a necessidade de manter arquivos sensíveis no repositório de código.
print("1", gcp_credentials_json)

if gcp_credentials_json:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_cred_file:
        temp_cred_file.write(gcp_credentials_json.encode("utf-8"))
        temp_cred_file_path = temp_cred_file.name
        print("2", temp_cred_file_path)
    # Cria um arquivo temporário para armazenar o JSON das credenciais.
    # Isso é necessário pois as APIs do Google esperam receber o caminho de um arquivo físico,
    # não uma string com o conteúdo do JSON.

    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(temp_cred_file_path)
    # Carrega as credenciais do arquivo JSON temporário utilizando a classe service_account.
    # O metodo from_service_account_file lê o arquivo JSON e retorna um objeto credencial.
    print("3", GS_CREDENTIALS)
    sys.exit(1)

else:
    cred_file = os.path.join(BASE_DIR, "credenciais.json")
    # Caso a variável de ambiente não esteja definida,
    # tenta carregar as credenciais a partir de um arquivo local 'credenciais.json' no diretório BASE_DIR.
    # Esta abordagem é recomendada apenas para desenvolvimento local e testes.
    print("4", cred_file)

    if os.path.exists(cred_file):
        GS_CREDENTIALS = service_account.Credentials.from_service_account_file(cred_file)
        # Se o arquivo existir, carrega as credenciais a partir dele.
        print("5", GS_CREDENTIALS)
    else:
        raise FileNotFoundError(
            "Arquivo credenciais.json não encontrado e variável GOOGLE_APPLICATION_CREDENTIALS_JSON não está definida."
        )
        # Caso nem o arquivo nem a variável de ambiente estejam disponíveis,
        # lança um erro para indicar a ausência das credenciais necessárias.

# -------------------------------------------------------------------
# Configurações do Google Cloud Storage para arquivos estáticos e mídia
# -------------------------------------------------------------------

GS_BUCKET_NAME = "django-render"
# Nome do bucket no Google Cloud Storage onde os arquivos serão armazenados.

STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/maria/"
MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
# URLs públicas para acesso direto a arquivos estáticos e de mídia hospedados no bucket GCS.
# O padrão da URL é o domínio oficial do GCS seguido do nome do bucket e pasta.

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
# Configuração de backends de armazenamento para Django usando django-storages.
# O dicionário STORAGES informa para onde e como armazenar arquivos:
# - 'default' é usado para arquivos de mídia enviados pelos usuários.
# - 'staticfiles' é usado para arquivos estáticos da aplicação (CSS, JS, imagens fixas).

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
# Define que os arquivos de mídia serão armazenados por padrão usando o backend GoogleCloudStorage.
# Isso faz com que o Django salve os uploads dos usuários diretamente no bucket configurado.

STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
# Essa é uma configuração do Django que define qual backend será usado para armazenar e servir os arquivos estáticos.
# Por padrão, o Django armazena os arquivos estáticos localmente (no servidor), mas em produção é comum usar serviços externos de armazenamento,
# como o Google Cloud Storage (GCS), Amazon S3, Azure Blob Storage, etc.
# Quando você define: STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage',
# você está dizendo para o Django que: Ao executar collectstatic, ao invés de copiar os arquivos para uma pasta local (como STATIC_ROOT),
# o Django vai fazer o upload diretamente para um bucket do Google Cloud Storage.

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Diretório local onde arquivos enviados pelos usuários serão salvos.
# Útil para desenvolvimento local e testes sem a necessidade de usar o bucket.

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Diretório onde os arquivos estáticos coletados (via collectstatic) serão salvos localmente.

# STATICFILES_DIRS = [
#    BASE_DIR / 'core' / 'static',
# ]
# Diretórios adicionais onde o Django procura arquivos estáticos, além dos apps.
# Normalmente usados para arquivos estáticos que não pertencem a nenhum app específico.
# Este trecho está comentado mas indica o caminho 'core/static' como fonte adicional.

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
