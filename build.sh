#!/bin/bash
# Atualiza e instala as dependências do projeto
pip install -r requirements.txt

# Executa as migrações do banco de dados
python manage.py migrate

# Coleta os arquivos estáticos para produção
python manage.py collectstatic --noinput

# Carrega os dados do arquivo backup.json
python manage.py loaddata backup.json

# Executa o comando customizado para sincronizar a pasta media local com o bucket Google Cloud Storage
python manage.py upload_media

# Esse comando é um comando padrão do Django usado para coletar todos os arquivos estáticos do projeto em um único lugar,
# para que possam ser servidos (disponibilizados) facilmente no ambiente de produção.
# Arquivos estáticos são os arquivos como CSS, JavaScript, imagens, fontes, ícones, etc.
# Eles normalmente ficam espalhados dentro de cada app Django, em pastas chamadas static/.
# Quando o comando abaixo é executado, o Django procura em todos os apps e diretórios de arquivos estáticos configurados,
# copia e junta todos esses arquivos em uma única pasta definida na configuração STATIC_ROOT.
python manage.py collectstatic

# Cria superusuário automaticamente, se não existir
# O código a seguir faz o seguinte:
# User.objects.filter(username='jcogfisica').exists() retorna True se já existir um usuário admin.
# or User.objects.create_superuser(...) só executa a criação se o retorno do .exists() for False.
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='jcogfisica').exists():
    User.objects.create_superuser('jcogfisica', 'jcogfisica@yahoo.com.br', 'MON010deo010')
EOF