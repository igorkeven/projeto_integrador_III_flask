from flask import Flask, render_template, request, flash, redirect, session
import mysql.connector



app = Flask(__name__)
app.config['SECRET_KEY'] = 'igorkeven'

def producao(x=True):
    global senhaBD 
    if x == False:
        
        senhaBD = 'senhaDoBancoDeDados'
        return app.run( host='www.StudyHub.com' , port=80)
    else:
        senhaBD = ''
        return app.run( debug=True , host='0.0.0.0' )





@app.route('/')
def login():
    if 'usuario' in session:
        del session['usuario']
   
    return render_template('login.html')







@app.route('/home')
def home():

    if 'usuario' in session: # SE TENTAR ENTRAR SEM LOGIN NAO CAI AQUI
        fundo = '/static/imagens/fundo.jpg' # FUNDO PROVISORIO DEPOIS PEGAR DO BD
        if not 'tema' in session: # DEPOIS APAGAR E PEGAR DADOS DO BD
            session['tema'] = '#3b5998'  # cor do tema padrão caso usuario nao tenha escolhido
        apostilas = ['apostila1.pdf','apostila2.pdf','apostila3.pdf','apostila4.pdf']# DEPOIS APAGAR E PEGAR DADOS DO BD
        return render_template('home.html', fundo=fundo, apostilas=apostilas, tema=session['tema'])
    else:
        flash('É necessario fazer login para acessar!!')
        return redirect('/')

@app.route('/sair')
def sair():
    session.clear() # LIMPA A SESSION E NAO PERMITE ENTRAR SEM LOGIN
    return redirect('/')








@app.route('/acesso', methods=['POST'])
def acesso():
    nome = request.form.get('username')
    senha = request.form.get('senha')

    

    if nome == 'asd' and senha == '123': # NOME E SENHA PROVISORIOS, DEPOIS COMPARAR COM DADOS DO BD
        session['usuario'] = nome # CRIA UMA SESSION USUARIO COM O NOME DO USUARIO DENTRO
        
        return redirect('/home')
    else:
        flash('nome e/ou senha invalidos , tente novamente!!')
        return redirect('/')



@app.route("/cadastro")
def cadastro():
    return render_template('cadastro.html')



@app.route("/cadastrar", methods=['POST'])
def cadastrar():

    nome = request.form.get('username')
    senha = request.form.get('senha')
    tema = ' #3b5998'
    img_capa = '/static/imagens/fundo.jpg'
    img_perfil = '/static/imagens/user.png'


    session['usuario'] = nome
    return redirect('/home')








@app.route('/mudarTema', methods=['POST'])
def mudarTema():
    
    tema = request.form.get('color')
    session['tema'] = tema # coloca o tema em uma session provisoriamente, DEPOIS MUDAR PARA SALVAR NO BANCO DE DADOS
    return redirect('/home')





@app.route("/novaSenha", methods=['POST'])
def novaSenha():
    novasenha = request.form.get('nova_senha')
    nome = session['usuario']  # Obtenha o nome do usuário da sessão

   

    flash('Senha alterada com sucesso')
    return redirect('/cliente')







# colocar o site no ar

if __name__ in '__main__':
    producao(True)
    #producao(False)

    
    # se a produção estiver True a aplicação esta em modo debug e no host localhome 
    # se estiver False esta no host www.kevenaom.com e modo debug off , preparado para o deploy na porta 80
    # e a senha do banco de dados muda
    # a função producao() esta no inicio do codigo
