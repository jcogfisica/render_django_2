from django.db import models
from pictures.models import PictureField

# SIGNALS
from django.db.models import signals
# Esta linha de código serve para importar o módulo de sinais (signals) do Django, que permite conectar funções a certos eventos que ocorrem no
# ciclo de vida dos modelos — como salvar, deletar, etc.
# O que são "signals" no Django?
# Signals são uma forma de Django permitir que diferentes partes do código “escutem” eventos e reajam a eles.
# Eles são úteis para executar ações automáticas quando algo acontece com um modelo, como:
# 1) Quando uma instância é salva;
# 2) Quando é deletada;
# 3) Quando o relacionamento many-to-many muda, etc.
from django.template.defaultfilters import slugify # importa a função slugify do Django, que serve para converter strings normais em “slugs” amigáveis para URLs.

# Esse código a seguir define uma classe abstrata chamada Base no Django, e ela é usada como modelo genérico reutilizável para outras models.
class Base(models.Model): # Define um modelo Django chamado Base. Ele herda de models.Model, então tem acesso ao ORM do Django.
    # A linha de código a seguir cria um campo de data/hora chamado criado.
    # O valor é preenchido automaticamente com a data/hora no momento em que o objeto for criado.
    # O atributo auto_now_add=True garante que esse valor não muda mais depois.
    criado = models.DateTimeField('Data de criação', auto_now_add=True)
    # A linha de código a seguir cria o campo modificado, também do tipo DateTimeField.
    # Esse campo é atualizado automaticamente toda vez que o objeto for salvo.
    # É útil para rastrear a última alteração.
    modificado = models.DateTimeField('Data de modificação', auto_now=True)
    # A linha a seguir cria um campo booleano chamado ativo. Serve para indicar se a instância está ativa ou não.
    # Pode ser usado como uma “flag de exclusão lógica”, onde o objeto não é deletado, apenas marcado como inativo.
    ativo = models.BooleanField('Ativo?', default=True)
    # Por fim, o código a seguir diz ao Django que a classe Base é abstrata. Ou seja: não vai gerar uma tabela no banco de dados.
    # É usada apenas como base para outras models, que vão herdar esses campos automaticamente.
    class Meta:
        abstract = True # A classe Base, que estende models.Model, é uma classe abstrata. Classe abstrata não pode ser criada em banco de dados: ela vai servir de rascunho para outras classes.

class Produto(Base): # Produto herda os atributos da classe Pai Base
    nome = models.CharField('Nome', max_length=100)
    preco = models.DecimalField('Preço', max_digits=8, decimal_places=2)
    estoque = models.IntegerField('Estoque')
    imagem = PictureField(upload_to='produtos',
        width_field="image_width",
        height_field="image_height",
        aspect_ratios=[None, "1/1"],
        # breakpoints={'thumb': 200, "mobile": 576, "desktop": 992},
        file_types=["PNG"],
        grid_columns=12,
        container_width=1200,
        pixel_densities=[1, 2],)
    image_width = models.PositiveIntegerField(null=True, editable=False)
    image_height = models.PositiveIntegerField(null=True, editable=False)
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    def __str__(self):
        return self.nome

# O trecho de código a seguir define uma função de signal no Django que cria automaticamente um slug a partir do nome de um produto antes de ele ser salvo
# no banco de dados.
def produto_pre_save(signal, instance, sender, *args, **kwargs):
    # Essa função será executada antes de salvar uma instância do modelo Produto.
    # Ela pega o valor de instance.nome, aplica o slugify() (converte para um formato URL-amigável) e atribui ao campo slug da instância.
    # Por exemplo, se instance.nome = "Camiseta Azul GG"
    # então, instance.slug = "camiseta-azul-gg"
    instance.slug = slugify(instance.nome)

# Sobre o código abaixo:
# signals.pre_save: sinal do Django que é emitido antes de um objeto ser salvo.
# connect(...): conecta a função produto_pre_save ao modelo Produto.
# Resultado: toda vez que um Produto for salvo, a função será executada automaticamente antes do save().
signals.pre_save.connect(produto_pre_save, sender=Produto)