"""
URL configuration for Django2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static # Importa a função static do módulo django.conf.urls.static, que é usada para ajudar a servir arquivos estáticos e de mídia durante o desenvolvimento.
from django.conf import settings # Importa o objeto settings do Django, que contém todas as configurações do seu projeto definidas no arquivo settings.py.

urlpatterns = [
    path('admin/', admin.site.urls),
    # Sobre a seguinte linha de código considere a pergunta: pictures.urls serve para quê?
    # A inclusão de path('pictures/', include('pictures.urls'))
    # é necessária porque a biblioteca django-pictures depende de algumas URLs internas para funcionar corretamente,
    # especialmente se você está usando recursos como:
    # 1. Placeholders: Imagens temporárias (ex: enquanto uma imagem real não foi carregada)
    # Se você tiver PICTURES["USE_PLACEHOLDERS"] = True, então essas rotas são obrigatórias.
    # 2. Preview de imagens ou URLs resolvidas automaticamente: Algumas views internas do pacote são usadas para servir essas
    # imagens em tempo real (por exemplo, para admin ou frontend dinâmico).
    path('pictures/', include('pictures.urls')),
    path('', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT): Essa parte adiciona ao urlpatterns rotas
# para servir os arquivos de mídia (imagens, uploads, etc) durante o desenvolvimento.
# Tal metodo usa o MEDIA_URL e MEDIA_ROOT configurados no seu settings.py.
# É importante para que imagens enviadas e outros arquivos de mídia fiquem acessíveis no navegador no ambiente de desenvolvimento.

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)