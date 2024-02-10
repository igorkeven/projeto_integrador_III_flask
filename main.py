from flask import Flask, render_template, request, flash, redirect, session
import mysql.connector
import os


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
        del session['id']
   
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
        
        # Buscar os dados dos amigos do usuário
        cursor.execute("""
            SELECT u.* 
            FROM usuario u
            INNER JOIN amigos a ON u.id = a.amigo_id
            WHERE a.usuario_id = %s
        """, (usuario[0],))

        amigos = cursor.fetchall()  # Obter todos os dados dos amigos

        # Buscar os dados dos usuários que não são amigos do usuário e não são o próprio usuário
        cursor.execute("""
            SELECT * 
            FROM usuario 
            WHERE id NOT IN (
                SELECT amigo_id 
                FROM amigos 
                WHERE usuario_id = %s
            )
            AND id != %s
        """, (usuario[0], usuario[0]))

        possiveis_amigos = cursor.fetchall()  # Obter todos os dados dos possíveis amigos

        cursor.execute("""
            SELECT u.* 
            FROM usuario u
            INNER JOIN solicitacoes_amizade s ON u.id = s.solicitante_id
            WHERE s.solicitado_id = %s
        """, (usuario[0],))

        solicitacoes_amizade = cursor.fetchall()

        # Fechar cursor e conexão com banco de dados
        cursor.close()
        mydb.close()
        
        if usuario is not None:  # Se encontramos um usuário que corresponde ao nome de usuário
            tema = usuario[3]  # Obtenha o tema do perfil do usuário
            img_perfil = usuario[4]  # Obtenha a imagem de perfil do usuário
            img_capa = usuario[5]  # Obtenha a imagem de capa do usuário
            # Aqui você pode adicionar o código para buscar as apostilas do usuário
            apostilas = ['apostila1.pdf','apostila2.pdf','apostila3.pdf','apostila4.pdf']  # DEPOIS APAGAR E PEGAR DADOS DO BD
            return render_template('home.html',solicitacoes_amizade=solicitacoes_amizade,possiveis_amigos=possiveis_amigos,nome=nome, fundo=img_capa, apostilas=apostilas, tema=tema,img_perfil=img_perfil, amigos=amigos)
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
        session['usuario'] = nome # CRIA UMA SESSION USUARIO COM O NOME DO USUARIO DENTRO
        session['id'] = usuario[0]  
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

    # Obter o ID do usuário que acabou de ser inserido
    usuario_id = cursor.lastrowid

    # Commit as mudanças
    mydb.commit()

    # Fechar cursor e conexão com banco de dados
    cursor.close()
    mydb.close()

    session['usuario'] = nome
    session['id'] = usuario_id  # Armazenar o ID do usuário na sessão

    return redirect('/home')




# rota para mudar o tema das cores


@app.route('/mudarTema', methods=['POST'])
def mudarTema():
    tema = request.form.get('color')
    nome = session['usuario']  # Obtenha o nome do usuário da sessão
    id = session['id'] 
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
    cursor.execute("UPDATE usuario SET tema = %s WHERE id = %s", (tema, id))

    # Commit as mudanças
    mydb.commit()

    # Fechar cursor e conexão com banco de dados
    cursor.close()
    mydb.close()
    flash('Tema alterado com sucesso')
    return redirect('/home')





@app.route("/novaSenha", methods=['POST'])
def novaSenha():
    novasenha = request.form.get('nova_senha')
    nome = session['usuario']  # Obtenha o nome do usuário da sessão
    id = session['id']
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
    cursor.execute("UPDATE usuario SET senha = %s WHERE id = %s", (novasenha, id))

    # Commit as mudanças
    mydb.commit()

    # Fechar cursor e conexão com banco de dados
    cursor.close()
    mydb.close()

    flash('Senha alterada com sucesso')
    return redirect('/home')



@app.route("/nova_capa", methods=['POST'])
def nova_capa():
    nova_capa = request.files.get('nova_capa')
    nome = session['usuario']  # Obtenha o nome do usuário da sessão
    id = session['id']

    nome_arquivo = f"Foto_capa_{nome}_{id}.{nova_capa.filename.split('.')[-1] }"
    nova_capa.save(os.path.join('static/imagens/fotosCapa/', nome_arquivo))
    nome_caminho = f"static/imagens/fotosCapa/{nome_arquivo}"

    

    # Criar uma conexão com o banco de dados
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=senhaBD,
    database="usuarios"
    )

    # Obter um cursor para executar consultas
    cursor = mydb.cursor()

    # Atualizar a capa no perfil do usuário
    cursor.execute("UPDATE usuario SET img_capa = %s WHERE id = %s", (nome_caminho, id))

    # Commit as mudanças
    mydb.commit()

    # Fechar cursor e conexão com banco de dados
    cursor.close()
    mydb.close()

    flash('Foto de capa alterada com sucesso')
    return redirect('/home')



# codiga para apagar a conta do usuario , apagando todos os dados e imagens relacionadas
@app.route('/apagar_conta', methods=['POST'])
def apagar_conta():
    if 'usuario' in session:  # SE TENTAR ENTRAR SEM LOGIN NAO CAI AQUI
        nome = session['usuario']  # Obtenha o nome do usuário da sessão
        id_usuario = session['id']

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
        cursor.execute("SELECT * FROM usuario WHERE id = %s", (id_usuario,))

        # Armazenar resultados da consulta em uma variável
        usuario = cursor.fetchone()

        # Remover as imagens de perfil e capa, verifica se não são as imagens padrão antes de apagar
        if usuario[4] != '/static/imagens/fundo.jpg':
            os.remove(usuario[4])  # img_capa
        if usuario[5] != '/static/imagens/user.png':
            os.remove(usuario[5])  # img_perfil

        # Remover os registros de amizade na tabela amigos
        cursor.execute("DELETE FROM amigos WHERE usuario_id = %s OR amigo_id = %s", (usuario[0], usuario[0]))

        # Remover o registro do usuário na tabela usuario
        cursor.execute("DELETE FROM usuario WHERE id = %s", (usuario[0],))

        # Commit as mudanças
        mydb.commit()

        # Fechar cursor e conexão com banco de dados
        cursor.close()
        mydb.close()

        # Remover o usuário da sessão
        session.pop('usuario', None)

        flash('Conta apagada com sucesso!!')
    else:
        flash('É necessário fazer login para acessar!!')

    return redirect('/')



# rota para adicionar o pedido de amizade para o amigo especifico no banco de dados
@app.route('/pedido_amizade', methods=['POST'])
def pedido_amizade():
    usuario_id = session['id']
    amigo_id = request.form.get('amigo_id')

    # Criar uma conexão com o banco de dados
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=senhaBD,
        database="usuarios"
    )

    # Obter um cursor para executar consultas
    cursor = mydb.cursor()

    # Inserir o pedido de amizade na tabela
    cursor.execute("INSERT INTO solicitacoes_amizade (solicitante_id, solicitado_id) VALUES (%s, %s)", (usuario_id, amigo_id))

    # Commit as mudanças
    mydb.commit()

    # Fechar cursor e conexão com banco de dados
    cursor.close()
    mydb.close()

    return redirect('/home')


# rota para adicionar o novo amigo no banco de dados oficializando a amizade
@app.route('/adicionar_amigo', methods=['POST'])
def adicionar_amigo():
    usuario_id = session['id']
    amigo_id = request.form.get('amigo_id')

    # Criar uma conexão com o banco de dados
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=senhaBD,
        database="usuarios"
    )

    # Obter um cursor para executar consultas
    cursor = mydb.cursor()

    # Remover o pedido de amizade da tabela
    cursor.execute("DELETE FROM solicitacoes_amizade WHERE solicitante_id = %s AND solicitado_id = %s", (amigo_id, usuario_id))

    # Adicionar a amizade na tabela de amigos
    cursor.execute("INSERT INTO amigos (usuario_id, amigo_id) VALUES (%s, %s)", (usuario_id, amigo_id))
    cursor.execute("INSERT INTO amigos (usuario_id, amigo_id) VALUES (%s, %s)", (amigo_id, usuario_id))

    # Commit as mudanças
    mydb.commit()

    # Fechar cursor e conexão com banco de dados
    cursor.close()
    mydb.close()

    return redirect('/home')



# area para negar o pedido de amizade e apagar o pedido do banco de dados
@app.route('/negar_amizade', methods=['POST'])
def negar_amizade():
    usuario_id = session['id']
    amigo_id = request.form.get('amigo_id')

    # Criar uma conexão com o banco de dados
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=senhaBD,
        database="usuarios"
    )

    # Obter um cursor para executar consultas
    cursor = mydb.cursor()

    # Remover o pedido de amizade da tabela
    cursor.execute("DELETE FROM solicitacoes_amizade WHERE solicitante_id = %s AND solicitado_id = %s", (amigo_id, usuario_id))

    # Commit as mudanças
    mydb.commit()

    # Fechar cursor e conexão com banco de dados
    cursor.close()
    mydb.close()

    return redirect('/home')



# colocar o site no ar

if __name__ in '__main__':
    producao(True)
    #producao(False)

    
    # se a produção estiver True a aplicação esta em modo debug e no host localhome 
    # se estiver False esta no host www.studyHub.com e modo debug off , preparado para o deploy na porta 80
    # e a senha do banco de dados muda
    # a função producao() esta no inicio do codigo
