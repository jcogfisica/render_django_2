# Cada aplicação django pode ter um arquivo forms.py. É neste arquivo que nós criamos os formulários

from django import forms
from django.forms import Textarea
from django.core.mail.message import EmailMessage # Classe que traz métodos e funções que permitem enviar emails

from .models import Produto # Importamos do módulo models a classe Produto

# O django tem um módulo forms o qual, por sua vez, possui uma classe chamada Form.
# Nossa classe ContatoForm irá herdar alguns atributos e métodos interessantes que serão utilizados em nossa aplicação: Herança da Orientação a Objetos
class ContatoForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100) # campo nome
    email = forms.EmailField(label='E-mail', max_length=100) # campo e-mail
    assunto = forms.CharField(label='Assunto', max_length=120) # campo assunto
    # campo mensagem: O atributo widget é preenchido com Textarea(), pois o CharField é um campo de entrada de texto de 1 linha;
    # só que para uma mensagem, este campo de texto de 1 linha não é suficiente. Com o atributo widget = Textarea(), temos uma caixa de texto com várias linhas.
    mensagem = forms.CharField(label='Mensagem', max_length=1000, widget=Textarea())

    def send_mail(self):
        nome = self.cleaned_data['nome'] # Recuperamos os dados inseridos nos campos do formulário
        email = self.cleaned_data['email']
        assunto = self.cleaned_data['assunto']
        mensagem = self.cleaned_data['mensagem']

        conteudo = f"Nome: {nome}\nE-mail: {email}\nAssunto: {assunto}\nMensagem: {mensagem}" # Montamos o conteúdo

        mail = EmailMessage(
            subject='E-mail enviado pelo sistema Django2.',
            body=conteudo,
            from_email='contato@seudominio.com.br',
            to=['contato@seudominio.com.br'],
            headers={'Reply-To': email}
        ) # Definimos o objeto mail da classe EmailMessage, passando os valores aos atributos

        mail.send() # Aplica o metodo send() ao objeto mail da classe EmailMessage definido acima

# forms.Form é uma classe base do Django para criar formulários manuais, isto é, sem vínculo direto com modelos.
# Usamos forms.Form quando:
# 1) Precisamos de um formulário simples (ex: contato, login)
# 2) Os dados não serão salvos diretamente no banco de dados via modelo
# 3) Necessitamos de controle total sobre os campos e a lógica
# forms.ModelForm, por sua vez, é uma subclasse de forms.Form, mas ligada a um modelo do Django (models.Model).
# Ela cria os campos do formulário automaticamente com base nos campos do modelo.
# Usamos forms.ModelForm quando:
# 1) Queremos criar/editar dados que serão salvos diretamente no banco
# 2) O formulário está relacionado a um models.Model
# 3) Queremos evitar repetir código já definido no modelo
# O seguinte código define um formulário baseado em modelo (ModelForm) no Django.
class ProdutoModelForm(forms.ModelForm): # Cria uma classe de formulário chamada ProdutoModelForm, que herda de forms.ModelForm. Isso indica que o formulário será gerado automaticamente com base no modelo Produto.
    class Meta: #  A classe interna Meta serve para configurar como o ModelForm se conecta ao modelo.
        model = Produto # model = Produto: indica que este formulário está associado ao modelo Produto.
        fields = ['nome', 'preco', 'estoque', 'imagem'] # fields = [...]: especifica quais campos do modelo serão exibidos no formulário.
