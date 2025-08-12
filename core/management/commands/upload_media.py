import os
# Biblioteca padrão do Python para interagir com o sistema operacional.
# Fornece funcionalidades para manipular caminhos de arquivos, navegar por diretórios,
# ler variáveis de ambiente, executar comandos do SO, entre outras operações.

from django.core.management.base import BaseCommand
# Importa a classe BaseCommand do módulo django.core.management.base.
# BaseCommand é a classe base para criar comandos customizados no Django.
# Esses comandos podem ser executados via manage.py e são úteis para tarefas administrativas,
# como sincronizar arquivos, limpar dados, gerar relatórios etc.

from google.cloud import storage
# Importa o módulo 'storage' da SDK oficial do Google Cloud.
# Essa biblioteca fornece classes e métodos para interagir com o Google Cloud Storage (GCS),
# que é o serviço de armazenamento de arquivos na nuvem do Google.
# Permite criar clientes, acessar buckets (containers de arquivos), criar blobs (arquivos),
# fazer upload, download, listagem e exclusão de arquivos no bucket.

from google.oauth2 import service_account
# Importa a classe service_account do pacote google.oauth2.
# Essa classe permite carregar credenciais (chaves) de uma conta de serviço do Google,
# normalmente armazenadas em arquivos JSON, para autenticar e autorizar acessos às APIs Google,
# como a do Cloud Storage. Essencial para operações seguras via SDK.


def upload_media_to_gcs(local_media_path, bucket_name, credentials, prefix='media'):
    """
    Função que sincroniza recursivamente os arquivos da pasta local_media_path (local)
    para o bucket do Google Cloud Storage (GCS) especificado, dentro da pasta prefix (padrão: 'media').

    Parâmetros:
    - local_media_path (str): Caminho absoluto ou relativo para a pasta local que contém os arquivos a enviar.
    - bucket_name (str): Nome do bucket GCS onde os arquivos serão armazenados.
    - credentials (google.oauth2.service_account.Credentials): Objeto contendo as credenciais para autenticação no GCS.
    - prefix (str): Prefixo/pasta dentro do bucket para organizar os arquivos. Por padrão 'media'.

    Essa função faz upload dos arquivos mantendo a estrutura de pastas relativa dentro do prefixo.
    """

    # Cria um cliente autenticado para se comunicar com o Google Cloud Storage.
    # O objeto 'client' é uma instância da classe google.cloud.storage.Client,
    # que representa o ponto de entrada para interagir com o serviço GCS.
    client = storage.Client(credentials=credentials)

    # Obtém uma referência ao bucket no GCS pelo nome fornecido.
    # 'bucket' é uma instância da classe google.cloud.storage.bucket.Bucket,
    # que representa um container lógico de objetos (arquivos) dentro do GCS.
    bucket = client.bucket(bucket_name)

    # Percorre a árvore de diretórios da pasta local_media_path usando os.walk do módulo os.
    # os.walk gera uma tupla (root, dirs, files) para cada diretório:
    # - root: caminho atual sendo percorrido,
    # - dirs: lista de subdiretórios dentro de root,
    # - files: lista de arquivos dentro de root.
    # Aqui usamos para processar todos os arquivos de forma recursiva.
    for root, dirs, files in os.walk(local_media_path):

        for file in files:
            # Junta o caminho do diretório atual 'root' com o nome do arquivo,
            # formando o caminho absoluto ou relativo completo para o arquivo local.
            local_path = os.path.join(root, file)

            # Calcula o caminho relativo do arquivo em relação ao diretório base local_media_path.
            # Isso é importante para preservar a estrutura de pastas ao enviar para o bucket.
            # Exemplo: se local_path = "media/uploads/img.jpg" e local_media_path = "media",
            # relative_path será "uploads/img.jpg".
            relative_path = os.path.relpath(local_path, local_media_path)

            # Gera o caminho final dentro do bucket, concatenando o prefixo com o caminho relativo do arquivo.
            # Substitui '\' por '/' para garantir compatibilidade com a forma Unix de caminhos no GCS,
            # pois GCS usa caminhos estilo URL (com '/').
            gcs_path = f"{prefix}/{relative_path.replace(os.sep, '/')}"

            # Cria um objeto Blob no bucket, que representa um arquivo armazenado em GCS.
            # A classe google.cloud.storage.blob.Blob encapsula funcionalidades para upload,
            # download e manipulação de arquivos no bucket.
            blob = bucket.blob(gcs_path)

            # Faz upload do arquivo local para o blob no bucket usando o caminho do arquivo local.
            # O metodo upload_from_filename lê o arquivo local e envia seu conteúdo para o GCS.
            blob.upload_from_filename(local_path)

            # Imprime no terminal uma mensagem indicando que o upload foi concluído para aquele arquivo.
            # Útil para monitorar o progresso do script durante a execução.
            print(f"Uploaded {local_path} to gs://{bucket_name}/{gcs_path}")


class Command(BaseCommand):
    """
    Classe que define o comando customizado Django para sincronizar arquivos locais da pasta 'media'
    com o bucket do Google Cloud Storage.

    - Essa classe herda de BaseCommand e deve estar localizada dentro de uma pasta
      'management/commands' de algum app Django para ser reconhecida.

    - Pode ser executada via linha de comando Django com:
      python manage.py sync_media
    """

    # Atributo de classe 'help' que fornece uma descrição curta do que o comando faz,
    # exibida quando o usuário roda `python manage.py help sync_media`.
    help = "Sincroniza a pasta media local com o bucket Google Cloud Storage."

    def handle(self, *args, **kwargs):
        """
        Metodo que é chamado automaticamente quando o comando é executado via manage.py.

        É o ponto de entrada do comando, onde a lógica de sincronização é implementada.
        """

        # Usa o módulo os para obter o diretório atual do processo (cwd = current working directory).
        # Junta com "media" para construir o caminho absoluto/local da pasta de mídia local.
        local_media_path = os.path.join(os.getcwd(), "media")

        # Define o nome do bucket GCS onde os arquivos serão enviados.
        bucket_name = "django-render"

        # Tenta obter o caminho do arquivo JSON de credenciais da conta de serviço Google.
        # Primeiro tenta ler a variável de ambiente 'GOOGLE_APPLICATION_CREDENTIALS' (padrão Google).
        # Se essa variável não estiver setada, assume que o arquivo 'credenciais.json' está na raiz do projeto.
        cred_file_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or "credenciais.json"

        # Usa o metodo from_service_account_file da classe Credentials para carregar
        # as credenciais da conta de serviço do arquivo JSON.
        # Essa classe é da biblioteca google.oauth2.service_account e representa as credenciais para autenticação.
        credentials = service_account.Credentials.from_service_account_file(cred_file_path)

        # Chama a função que faz o upload dos arquivos da pasta local para o bucket,
        # passando o caminho local, nome do bucket e as credenciais carregadas.
        upload_media_to_gcs(local_media_path, bucket_name, credentials)

        # Escreve uma mensagem colorida de sucesso na saída padrão do Django,
        # usando os utilitários do BaseCommand (self.stdout.write + self.style.SUCCESS).
        self.stdout.write(self.style.SUCCESS("Sincronização concluída com sucesso!"))
