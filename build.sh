#!/bin/bash
set -e  # Faz o script parar imediatamente se algum comando retornar erro (boa prática para evitar deploys parcialmente concluídos).

echo "Instalando dependências"
# Atualiza e instala as dependências do projeto
pip install -r requirements.txt
# Instala todas as bibliotecas Python necessárias, conforme definido no requirements.txt.
# Essencial para garantir que o ambiente tenha as bibliotecas usadas pelo projeto.

echo "Executando migrações"
# Executa as migrações do banco de dados
python manage.py migrate --noinput
# Aplica todas as migrações pendentes no banco de dados, atualizando a estrutura para a versão atual do código.
# --noinput evita prompts interativos, essencial em deploys automáticos.

echo "Coletando arquivos estáticos"
# Coleta todos os arquivos estáticos do projeto para o diretório STATIC_ROOT, definido nas configurações do Django.
# Essa ação consolida arquivos CSS, JS, imagens e outros recursos em um único local para serem servidos no ambiente de produção.
python manage.py collectstatic --noinput
# O parâmetro --noinput previne que o comando pause pedindo confirmação.

echo "Carregando dados iniciais"
# Carrega dados fixos iniciais no banco a partir de um arquivo JSON
python manage.py loaddata backup.json
# Útil para importar fixtures com dados essenciais, como categorias, configurações, ou usuários base.

echo "Sincronizando mídia com bucket GCS"
# Comando customizado que sincroniza a pasta local media com o bucket do Google Cloud Storage
python manage.py upload_media
# Garante que as mídias carregadas localmente estejam disponíveis no bucket.
# Essencial para que imagens e outros arquivos de mídia sejam acessíveis em produção.
# Atenção: certifique-se que este comando esteja implementado para subir o conteudo completo necessario.

echo "Criando superusuário se não existir"
# Cria superusuário automaticamente se ainda não existir.
python manage.py shell << EOF
from django.contrib.auth.models import User
# Verifica se o usuário admin já existe para evitar duplicidade
if not User.objects.filter(username='jcogfisica').exists():
    # Cria superusuário com credenciais definidas
    User.objects.create_superuser('jcogfisica', 'jcogfisica@yahoo.com.br', 'MON010deo010')
EOF

echo "Build concluído!"