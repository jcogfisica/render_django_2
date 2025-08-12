from django.shortcuts import render, redirect
from django.contrib import messages # Permite que sejam exibidas mensagens no contexto de nossa página/aplicação

from .forms import ContatoForm, ProdutoModelForm
from .models import Produto

# View 1
def index(request):
    # Aqui é criado um dicionário chamado context que será passado para o template.
    # 'produtos' é a chave que o template usará para acessar os dados.
    # Produto.objects.all() → busca todos os registros da tabela Produto no banco de dados (o modelo Produto provavelmente está definido no models.py).
    # Ou seja, context["produtos"] conterá uma lista/QuerySet com todos os produtos.
    context = {
        'produtos': Produto.objects.all(),
    }
    # A seguinte linha de código faz o seguinte:
    # 1) Recebe o request: É o objeto que representa a requisição HTTP feita pelo navegador (inclui informações como metodo, parâmetros, cookies etc.).
    # O Django exige passar o request para poder processar a resposta corretamente.
    # 2) Renderiza o template 'index.html': O Django procura o arquivo index.html na pasta de templates do projeto.
    # Esse HTML pode conter tags do Django como {% for %} ou {{ variável }}, que serão processadas antes do envio ao navegador.
    # 3) Passa dados para o template usando context: O context é um dicionário com variáveis que o template pode usar.
    # Em nosso caso, context = {'produtos': Produto.objects.all()} significa que, no HTML, você pode acessar {{ produtos }} e iterar sobre ele com {% for produto in produtos %}.
    return render(request, 'index.html', context = context)

# View 2
def contato(request):
    form = ContatoForm(request.POST or None) # Nosso objeto form pode ser um formulário preenchido ou vazio. Nosso form pode conter dados ou não. Conterá dados quando o usuário preencher o formulário e pressionar o botão "submit"; não conterá dados quando o usuário simplesmente carregar a página de contato

    if str(request.method) == 'POST': # Se o usuário preencheu corretamente o formulário e pressionou o botão "submit"
        if str(form.is_valid()): # Objetos da classe forms.Form têm o metodo is_valid(): este metodo retorna True se o formulario nao tem erros e False, caso contrario. Para um formulario nao conter erros todos os campos devem estar devidamente preenchidos e o token de seguranca deve estar ok.
            # print(f"POST: {request.POST}")
            # nome = form.cleaned_data['nome'] # Metodo que armazena o valor submetido em um campo (para uma determinada chave informada) em uma variavel
            # email = form.cleaned_data['email']
            # assunto = form.cleaned_data['assunto']
            # mensagem = form.cleaned_data['mensagem']

            # print("Mensagem enviada")
            # print(f"Nome: {nome}")
            # print(f"Email: {email}")
            # print(f"Assunto: {assunto}")
            # print(f"Mensagem: {mensagem}")
            form.send_mail() # Metodo da classe ContatoForm importada de forms.py e definida neste módulo: aqui enviamos o email.
            messages.success(request, 'Formulário enviado com sucesso!') # Exibe uma mensagem de sucesso ao submeter o formulário
            form = ContatoForm() # Limpa o formulário
        else:
            messages.error(request, 'Erro ao enviar formulário!') # Exibe uma mensagem de erro

    context = {
        'form': form,
    }
    return render(request, 'contato.html', context)

# View 3
def produto(request): # Define uma view Django chamada produto que recebe o objeto request.
    if str(request.user) != "AnonymousUser":
        if str(request.method) == 'POST': # Verifica se o metodo HTTP da requisição é POST (ou seja, envio de dados pelo formulário).
            form = ProdutoModelForm(request.POST, request.FILES) # Cria uma instância do formulário ProdutoModelForm passando: 1) request.POST — dados do formulário enviados; 2) request.FILES — arquivos enviados (ex: imagem).
            if form.is_valid(): # Valida o formulário (checa se os dados estão corretos conforme regras do modelo e do formulário).
                # prod = form.save(commit=False) # Cria o objeto prod do modelo Produto, mas ainda não salva no banco (commit=False).
                # As 4 linhas de código a seguir imprimem no console os dados do produto (nome, preço, estoque, imagem).
                # print(f"Nome: {prod.nome}")
                # print(f"Preco: {prod.preco}")
                # print(f"Estoque: {prod.estoque}")
                # print(f"Imagem: {prod.imagem}")

                form.save(commit = True) # Salva a forma no banco de dados

                messages.success(request, "Produto adicionado com sucesso!") # Adiciona uma mensagem de sucesso que pode ser exibida no template (usando o framework de mensagens do Django).
            else:
                messages.error(request, "Erro ao adicionar produto!") # Caso o formulário não seja válido, adiciona uma mensagem de erro para o usuário.

        form = ProdutoModelForm() # Cria um formulário vazio para ser exibido.

        context = {
            'form': form,
        } # Prepara o contexto para enviar ao template, com o formulário (seja vazio ou preenchido).
        return render(request, 'produto.html', context) # Renderiza o template produto.html, enviando o contexto com o formulário.
    else:
        return redirect("index") # O usuário só será permitido preencher o formulário se estiver logado/autenticado; caso contrário, ao tentar acessá-lo será redirecionado para a página index.html
