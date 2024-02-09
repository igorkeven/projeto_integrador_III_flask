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
    if 'usuario' in session:  # SE TENTAR ENTRAR SEM LOGIN NAO CAI AQUI
        nome = session['usuario']  # Obtenha o nome do usuário da sessão

        # Criar uma conexão com o banco de dados
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=senhaBD,
        database="usuarios"
        )

        # Obter um cursor para executar consultas
        cursor = mydb.cursor()

        # Buscar os dados do usuário no banco de dados
        cursor.execute("SELECT * FROM usuario WHERE nome = %s", (nome,))

        # Armazenar resultados da consulta em uma variável
        usuario = cursor.fetchone()

        # Fechar cursor e conexão com banco de dados
        cursor.close()
        mydb.close()
        print(usuario)
        if usuario is not None:  # Se encontramos um usuário que corresponde ao nome de usuário
            tema = usuario[3]  # Obtenha o tema do perfil do usuário
            img_perfil = usuario[4]  # Obtenha a imagem de perfil do usuário
            img_capa = usuario[5]  # Obtenha a imagem de capa do usuário
            # Aqui você pode adicionar o código para buscar as apostilas do usuário
            apostilas = ['apostila1.pdf','apostila2.pdf','apostila3.pdf','apostila4.pdf']  # DEPOIS APAGAR E PEGAR DADOS DO BD
            return render_template('home.html', fundo=img_capa, apostilas=apostilas, tema=tema,img_perfil=img_perfil)
        else:
            flash('Erro ao buscar os dados do usuário!!')
            return redirect('/')
    else:
        flash('É necessario fazer login para acessar!!')
        return redirect('/')





@app.route('/sair')
def sair():
    session.clear() # LIMPA A SESSION E NAO PERMITE ENTRAR SEM LOGIN
    return redirect('/')



# rota para acesso com utilização de banco de dados
@app.route('/acesso', methods=['POST'])
def acesso():
    nome = request.form.get('username')
    senha = request.form.get('senha')

    # processamento dos dados
    # Criar uma conexão com o banco de dados
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=senhaBD,
    database="usuarios"
    )

    # Obter um cursor para executar consultas
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM usuario WHERE nome = %s AND senha = %s", (nome, senha))

    # Armazenar resultados da consulta em uma variável
    usuario = cursor.fetchone()

    # Fechar cursor e conexão com banco de dados
    cursor.close()
    mydb.close()

    if usuario is not None:  # Se encontramos um usuário que corresponde ao nome de usuário e senha
        session['usuario'] = nome  # CRIA UMA SESSION USUARIO COM O NOME DO USUARIO DENTRO
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


 # processamento dos dados
    # Criar uma conexão com o banco de dados
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=senhaBD,
    database="usuarios"
    )

    # Obter um cursor para executar consultas
    cursor = mydb.cursor()


    # Inserir dados na tabela usuario
    cursor.execute("insert into usuario (nome, senha, tema, img_perfil, img_capa ) values (%s, %s, %s, %s, %s)", (nome, senha, tema, img_perfil, img_capa))


    # Commit as mudanças
    mydb.commit()

    # Armazenar resultados da consulta em uma variável
    usuarios = cursor.fetchall()

    # Fechar cursor e conexão com banco de dados
    cursor.close()
    mydb.close()
    session['usuario'] = nome
    return redirect('/home')





# rota para mudar o tema das cores


@app.route('/mudarTema', methods=['POST'])
def mudarTema():
    tema = request.form.get('color')
    nome = session['usuario']  # Obtenha o nome do usuário da sessão

    # Criar uma conexão com o banco de dados
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=senhaBD,
    database="usuarios"
    )

    # Obter um cursor para executar consultas
    cursor = mydb.cursor()

    # Atualizar o tema no perfil do usuário
    cursor.execute("UPDATE usuario SET tema = %s WHERE nome = %s", (tema, nome))

    # Commit as mudanças
    mydb.commit()

    # Fechar cursor e conexão com banco de dados
    cursor.close()
    mydb.close()

    return redirect('/home')





@app.route("/novaSenha", methods=['POST'])
def novaSenha():
    novasenha = request.form.get('nova_senha')
    nome = session['usuario']  # Obtenha o nome do usuário da sessão

    # Criar uma conexão com o banco de dados
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=senhaBD,
    database="usuarios"
    )

    # Obter um cursor para executar consultas
    cursor = mydb.cursor()

    # Atualizar a senha no perfil do usuário
    cursor.execute("UPDATE usuario SET senha = %s WHERE nome = %s", (novasenha, nome))

    # Commit as mudanças
    mydb.commit()

    # Fechar cursor e conexão com banco de dados
    cursor.close()
    mydb.close()

    flash('Senha alterada com sucesso')
    return redirect('/cliente')







# colocar o site no ar

if __name__ in '__main__':
    producao(True)
    #producao(False)

    
    # se a produção estiver True a aplicação esta em modo debug e no host localhome 
    # se estiver False esta no host www.studyHub.com e modo debug off , preparado para o deploy na porta 80
    # e a senha do banco de dados muda
    # a função producao() esta no inicio do codigo
