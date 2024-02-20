import sqlite3

# Conecte-se ao banco de dados SQLite (será criado se não existir)
conn = sqlite3.connect('usuarios.db')

# Crie um cursor para executar comandos SQL
cursor = conn.cursor()

# Crie a tabela usuario
cursor.execute("""
CREATE TABLE usuario (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    senha TEXT NOT NULL,
    tema TEXT DEFAULT '#3b5998',
    img_perfil TEXT DEFAULT '/static/imagens/user.png',
    img_capa TEXT DEFAULT '/static/imagens/fundo.jpg'
)
""")



# Crie a tabela amigos
cursor.execute("""
CREATE TABLE amigos (
    usuario_id INTEGER,
    amigo_id INTEGER,
    PRIMARY KEY (usuario_id, amigo_id),
    FOREIGN KEY(usuario_id) REFERENCES usuario(id),
    FOREIGN KEY(amigo_id) REFERENCES usuario(id)
)
""")

# Crie a tabela solicitacoes_amizade
cursor.execute("""
CREATE TABLE solicitacoes_amizade (
    solicitante_id INTEGER,
    solicitado_id INTEGER,
    PRIMARY KEY (solicitante_id, solicitado_id),
    FOREIGN KEY(solicitante_id) REFERENCES usuario(id),
    FOREIGN KEY(solicitado_id) REFERENCES usuario(id)
)
""")

# Criar a tabela desafios
cursor.execute("""
CREATE TABLE desafios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    pergunta TEXT,
    respostaA TEXT,
    respostaB TEXT,
    respostaC TEXT,
    respostaD TEXT,
    respostaCERTA TEXT,
    categoria TEXT,
    dificuldade INTEGER
)
""")

# Commit as mudanças
conn.commit()

# Fechar cursor e conexão com banco de dados
cursor.close()
conn.close()