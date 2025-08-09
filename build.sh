#!/bin/bash
# Atualiza e instala as dependências do projeto
pip install -r requirements.txt

# Executa as migrações do banco de dados
python manage.py migrate

# Coleta os arquivos estáticos para produção
python manage.py collectstatic --noinput

# Carrega os dados do arquivo backup.json
python manage.py loaddata backup.json

# Cria superusuário automaticamente, se não existir
# O código a seguir faz o seguinte:
# User.objects.filter(username='jcogfisica').exists() retorna True se já existir um usuário admin.
# or User.objects.create_superuser(...) só executa a criação se o retorno do .exists() for False.
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='jcogfisica').exists():
    User.objects.create_superuser('jcogfisica', 'jcogfisica@yahoo.com.br', 'MON010deo010')
EOF