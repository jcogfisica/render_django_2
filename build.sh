#!/bin/bash
# Atualiza e instala as dependências do projeto
pip install -r requirements.txt

# Executa as migrações do banco de dados
python manage.py migrate

# Coleta os arquivos estáticos para produção
python manage.py collectstatic --noinput

# Carrega os dados do arquivo backup.json
python manage.py loaddata backup.json