import sqlite3
from flask import g

DATABASE = 'pizzabyte.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Tabela de pizzas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pizzas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT NOT NULL,
                preco REAL NOT NULL,
                imagem TEXT NOT NULL
            )
        ''')
        
        # Tabela de itens do carrinho
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carrinho (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pizza_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (pizza_id) REFERENCES pizzas (id)
            )
        ''')
        
        # Inserir pizzas padrão se a tabela estiver vazia
        cursor.execute('SELECT COUNT(*) FROM pizzas')
        if cursor.fetchone()[0] == 0:
            pizzas = [
                ('Calabresa', 'Mussarela, calabresa, cebola, azeitonas e orégano', 39.90, 'img/calabresa.png'),
                ('Frango', 'Mussarela, frango desfiado, milho verde e tomate', 36.90, 'img/frango.png'),
                ('Portuguesa', 'Mussarela, presunto, ovo, pimentão, azeitonas, cebola, tomate e orégano', 42.90, 'img/portuguesa.png'),
                ('Bacon', 'Mussarela, presunto, bacon e orégano', 39.90, 'img/bacon.png')
            ]
            cursor.executemany('INSERT INTO pizzas (nome, descricao, preco, imagem) VALUES (?, ?, ?, ?)', pizzas)

        # Tabela de pedidos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_pedido TEXT NOT NULL UNIQUE,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'Em preparo',
                total REAL NOT NULL,
                cliente_nome TEXT NOT NULL,
                cliente_endereco TEXT NOT NULL,
                cliente_celular TEXT NOT NULL,
                forma_pagamento TEXT NOT NULL,
                observacoes TEXT
            )
        ''')

        # Tabela de itens do pedido
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_pedido TEXT NOT NULL UNIQUE,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'Em preparo',
                total REAL NOT NULL,
                cliente_nome TEXT NOT NULL,
                cliente_endereco TEXT NOT NULL,
                cliente_celular TEXT NOT NULL,
                forma_pagamento TEXT NOT NULL,
                observacoes TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS itens_pedido (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER NOT NULL,
                pizza_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario REAL NOT NULL,
                FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
                FOREIGN KEY (pizza_id) REFERENCES pizzas (id)
        )
    ''')
        
        
        db.commit()

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()