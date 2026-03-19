from flask import Flask, render_template, request, redirect, url_for, session, g, flash
import sqlite3
import random
import string
from datetime import datetime
from collections import deque
from database import get_db, init_db, close_connection

app = Flask(__name__, static_folder='static', template_folder='templates')
import os
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_local')
app.config['DATABASE'] = 'pizzabyte.db'

# Configuração do banco de dados
app.teardown_appcontext(close_connection)

# Inicializar banco de dados
with app.app_context():
    init_db(app)

# Estruturas dinâmicas
fila_pedidos = deque()
pilha_cancelados = []

def gerar_numero_pedido():
    letras = random.choices(string.ascii_uppercase, k=2)
    numeros = random.choices(string.digits, k=4)
    return f"{''.join(letras)}{''.join(numeros)}"

# Função recursiva
def soma_total_recursiva(itens, index=0):
    if index >= len(itens):
        return 0
    return itens[index]['preco'] * itens[index]['quantidade'] + soma_total_recursiva(itens, index + 1)

# Algoritmos de ordenação
def bubble_sort(pizzas):
    n = len(pizzas)
    for i in range(n):
        for j in range(0, n - i - 1):
            if pizzas[j]['preco'] > pizzas[j + 1]['preco']:
                pizzas[j], pizzas[j + 1] = pizzas[j + 1], pizzas[j]
    return pizzas

def insertion_sort(pizzas):
    for i in range(1, len(pizzas)):
        key = pizzas[i]
        j = i - 1
        while j >= 0 and key['nome'] < pizzas[j]['nome']:
            pizzas[j + 1] = pizzas[j]
            j -= 1
        pizzas[j + 1] = key
    return pizzas

# Rotas Públicas
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cardapio')
def cardapio():
    db = get_db()
    pizzas = db.execute('SELECT * FROM pizzas').fetchall()
    return render_template('cardapio.html', pizzas=pizzas)

@app.route('/ordenar_pizzas/<criterio>')
def ordenar_pizzas(criterio):
    db = get_db()
    pizzas = db.execute('SELECT * FROM pizzas').fetchall()
    pizzas = [dict(p) for p in pizzas]

    if criterio == 'preco':
        pizzas = bubble_sort(pizzas)
    elif criterio == 'nome':
        pizzas = insertion_sort(pizzas)

    return render_template('cardapio.html', pizzas=pizzas)

@app.route('/fazer_pedido_manual')
def fazer_pedido_manual():
    pedido = {'numero': gerar_numero_pedido(), 'status': 'Em preparo'}
    fila_pedidos.append(pedido)
    flash(f'Pedido {pedido["numero"]} adicionado à fila!', 'success')
    return redirect(url_for('home'))

@app.route('/cancelar_pedido_manual')
def cancelar_pedido_manual():
    if fila_pedidos:
        pedido = fila_pedidos.popleft()
        pilha_cancelados.append(pedido)
        flash(f'Pedido {pedido["numero"]} cancelado e movido para a pilha!', 'info')
    else:
        flash('Nenhum pedido na fila para cancelar.', 'warning')
    return redirect(url_for('home'))

from datetime import datetime, timedelta

@app.route('/relatorios')
def relatorios():
    db = get_db()
    
    # Calcula a data de 30 dias atrás
    data_limite = datetime.now() - timedelta(days=30)
    
    # Consulta pedidos dos últimos 30 dias (mesmo após limpeza)
    total_pedidos = db.execute('''
        SELECT COUNT(*) as total FROM pedidos 
        WHERE data >= ?
    ''', (data_limite,)).fetchone()['total']
    
    receita_total = db.execute('''
        SELECT SUM(total) as receita FROM pedidos 
        WHERE data >= ?
    ''', (data_limite,)).fetchone()['receita'] or 0
    
    pizza_mais_vendida = db.execute('''
        SELECT p.nome, SUM(ip.quantidade) as total_vendida 
        FROM itens_pedido ip 
        JOIN pizzas p ON ip.pizza_id = p.id 
        JOIN pedidos ped ON ip.pedido_id = ped.id
        WHERE ped.data >= ?
        GROUP BY p.id 
        ORDER BY total_vendida DESC 
        LIMIT 1
    ''', (data_limite,)).fetchone()
    
    media_pedidos = receita_total / total_pedidos if total_pedidos else 0
    
    return render_template('relatorios.html',
                         total_pedidos=total_pedidos,
                         receita_total=receita_total,
                         media_pedidos=media_pedidos,
                         pizza_mais_vendida=pizza_mais_vendida)

# Rotas de Pedidos
@app.route('/meus_pedidos')
def meus_pedidos():
    db = get_db()
    pedidos = db.execute('''
        SELECT *, datetime(data) as data_formatada 
        FROM pedidos 
        ORDER BY data DESC
        LIMIT 10
    ''').fetchall()

    pedidos_com_itens = []
    for pedido in pedidos:
        itens = db.execute('''
            SELECT p.nome, ip.quantidade, ip.preco_unitario, p.imagem
            FROM itens_pedido ip
            JOIN pizzas p ON ip.pizza_id = p.id
            WHERE ip.pedido_id = ?
        ''', (pedido['id'],)).fetchall()
        pedidos_com_itens.append({'pedido': pedido, 'itens': itens})

    return render_template('pedido.html', pedidos_com_itens=pedidos_com_itens)

@app.route('/finalizar_pedido', methods=['POST'])
def finalizar_pedido():
    db = get_db()
    try:
        itens_carrinho = db.execute('''
            SELECT c.id, p.id as pizza_id, p.nome, p.preco, c.quantidade 
            FROM carrinho c 
            JOIN pizzas p ON c.pizza_id = p.id
        ''').fetchall()

        if not itens_carrinho:
            flash('Seu carrinho está vazio!', 'warning')
            return redirect(url_for('carrinho'))

        total = sum(item['preco'] * item['quantidade'] for item in itens_carrinho) + 10.00
        numero_pedido = gerar_numero_pedido()

        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO pedidos (
                numero_pedido, total, status,
                cliente_nome, cliente_endereco,
                cliente_celular, forma_pagamento
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            numero_pedido, total, 'Em preparo',
            'Cliente Padrão', 'Endereço não informado',
            '000000000', 'Dinheiro'
        ))
        pedido_id = cursor.lastrowid

        for item in itens_carrinho:
            cursor.execute('''
                INSERT INTO itens_pedido (pedido_id, pizza_id, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?)
            ''', (pedido_id, item['pizza_id'], item['quantidade'], item['preco']))

        db.execute('DELETE FROM carrinho')
        db.commit()

        flash(f'Pedido #{numero_pedido} realizado com sucesso!', 'success')
        return redirect(url_for('meus_pedidos'))

    except Exception as e:
        db.rollback()
        flash(f'Erro ao finalizar pedido: {str(e)}', 'danger')
        return redirect(url_for('carrinho'))

# Rotas de Autenticação
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Rotas Administrativas
@app.route('/admin/pedidomanual')
def pedidomanual():
    db = get_db()
    pizzas = db.execute('SELECT * FROM pizzas').fetchall()
    return render_template('pedidomanual.html', pizzas=pizzas)

@app.route('/admin/verpedido')
def verpedido():
    db = get_db()
    pedidos = db.execute('SELECT * FROM pedidos ORDER BY data DESC').fetchall()
    return render_template('verpedido.html', pedidos=pedidos)

@app.route('/atualizar_status/<int:pedido_id>', methods=['POST'])
def atualizar_status(pedido_id):
    db = get_db()
    novo_status = request.form.get('novo_status')

    try:
        db.execute('UPDATE pedidos SET status = ? WHERE id = ?', (novo_status, pedido_id))
        db.commit()
        flash('Status do pedido atualizado com sucesso!', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Erro ao atualizar status: {str(e)}', 'danger')

    return redirect(url_for('verpedido'))

# Rotas de Manipulação do Carrinho
@app.route('/carrinho')
def carrinho():
    db = get_db()
    itens_carrinho = db.execute('''
        SELECT c.id, p.id as pizza_id, p.nome, p.descricao, p.preco, p.imagem, c.quantidade 
        FROM carrinho c 
        JOIN pizzas p ON c.pizza_id = p.id
    ''').fetchall()

    subtotal = sum(item['preco'] * item['quantidade'] for item in itens_carrinho) if itens_carrinho else 0
    taxa_entrega = 10.00
    total = subtotal + taxa_entrega

    return render_template('carrinho.html', 
                         itens_carrinho=itens_carrinho,
                         subtotal=subtotal,
                         taxa_entrega=taxa_entrega,
                         total=total,
                         total_itens=len(itens_carrinho))

@app.route('/adicionar_carrinho/<int:pizza_id>', methods=['POST'])
def adicionar_carrinho(pizza_id):
    db = get_db()
    item = db.execute('SELECT * FROM carrinho WHERE pizza_id = ?', (pizza_id,)).fetchone()

    if item:
        db.execute('UPDATE carrinho SET quantidade = quantidade + 1 WHERE id = ?', (item['id'],))
    else:
        db.execute('INSERT INTO carrinho (pizza_id, quantidade) VALUES (?, 1)', (pizza_id,))

    db.commit()
    flash('Item adicionado ao carrinho!', 'success')
    return redirect(url_for('cardapio'))

@app.route('/remover_item/<int:item_id>', methods=['POST'])
def remover_item(item_id):
    db = get_db()
    db.execute('DELETE FROM carrinho WHERE id = ?', (item_id,))
    db.commit()
    flash('Item removido do carrinho', 'info')
    return redirect(url_for('carrinho'))

@app.route('/atualizar_quantidade/<int:item_id>', methods=['POST'])
def atualizar_quantidade(item_id):
    nova_quantidade = request.form.get('quantidade', type=int)
    if nova_quantidade and nova_quantidade > 0:
        db = get_db()
        db.execute('UPDATE carrinho SET quantidade = ? WHERE id = ?', (nova_quantidade, item_id))
        db.commit()
        flash('Quantidade atualizada', 'success')
    else:
        flash('Quantidade inválida', 'danger')
    return redirect(url_for('carrinho'))

@app.route('/admin/processar_pedidomanual', methods=['POST'])
def processar_pedidomanual():
    db = get_db()
    try:
        nome = request.form.get('nome', 'Cliente não identificado')
        endereco = request.form.get('endereco', 'Endereço não informado')
        celular = request.form.get('celular', '000000000')
        forma_pagamento = request.form.get('pagamento', 'Dinheiro')
        observacoes = request.form.get('observacoes', '')

        pizzas_ids = request.form.getlist('pizzas')
        quantidades = request.form.getlist('quantidades')

        if not pizzas_ids:
            flash('Nenhuma pizza selecionada!', 'danger')
            return redirect(url_for('pedidomanual'))

        total = 10.00
        itens = []
        for pizza_id, quantidade in zip(pizzas_ids, quantidades):
            pizza = db.execute('SELECT preco FROM pizzas WHERE id = ?', (pizza_id,)).fetchone()
            if pizza:
                preco = pizza['preco']
                total += preco * int(quantidade)
                itens.append({
                    'pizza_id': pizza_id,
                    'quantidade': int(quantidade),
                    'preco': preco
                })

        numero_pedido = gerar_numero_pedido()

        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO pedidos (
                numero_pedido, total, status,
                cliente_nome, cliente_endereco,
                cliente_celular, forma_pagamento, observacoes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            numero_pedido, total, 'Em preparo',
            nome, endereco,
            celular, forma_pagamento, observacoes
        ))
        pedido_id = cursor.lastrowid

        for item in itens:
            cursor.execute('''
                INSERT INTO itens_pedido (pedido_id, pizza_id, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?)
            ''', (item['pizza_id'], item['quantidade'], item['preco'], item['preco']))

        db.commit()
        flash(f'Pedido #{numero_pedido} criado com sucesso! Total: R$ {total:.2f}', 'success')
        return redirect(url_for('verpedido'))

    except Exception as e:
        db.rollback()
        flash(f'Erro ao processar pedido: {str(e)}', 'danger')
        return redirect(url_for('pedidomanual'))
    
@app.route('/limpar_pedidos', methods=['POST'])
def limpar_pedidos():
    db = get_db()
    try:
        # Limpa a fila de pedidos e a pilha de cancelados (opcional)
        fila_pedidos.clear()
        pilha_cancelados.clear()
        
        # Opção 1: Limpar apenas pedidos com status "Entregue" ou "Cancelado" do banco de dados
        db.execute('DELETE FROM pedidos WHERE status IN ("Entregue", "Cancelado")')
        
        # Opção 2 (alternativa): Limpar TODOS os pedidos (use com cautela!)
        # db.execute('DELETE FROM pedidos')
        
        db.commit()
        flash('Pedidos finalizados/cancelados foram removidos!', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Erro ao limpar pedidos: {str(e)}', 'danger')
    return redirect(url_for('verpedido'))

if __name__ == '__main__':
    app.run(debug=True)
