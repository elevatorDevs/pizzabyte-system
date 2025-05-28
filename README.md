# 🍕 Sistema de Gerenciamento para Pizzaria

Este sistema foi desenvolvido como parte de um trabalho acadêmico para os cursos Banco de Dados e Estrutura de dados da Universidade do Distrito Federal (UDF). Seu objetivo é simular o funcionamento de uma pizzaria, integrando **programação orientada a objetos**, **estrutura de dados**, **desenvolvimento web com Flask**, e **banco de dados SQLite** em uma aplicação web funcional.

---

## 🎯 Objetivos do Projeto

O sistema tem como propósito:

- Gerenciar o cardápio de pizzas com seus respectivos preços, descrições e imagens.
- Permitir que os usuários visualizem o cardápio e adicionem pizzas ao carrinho.
- Controlar pedidos utilizando estruturas de dados como **fila (pedidos)** e **pilha (cancelamentos)**.
- Calcular o valor total do pedido usando **função recursiva**.
- Ordenar pizzas utilizando algoritmos clássicos como **Bubble Sort** (por preço) e **Insertion Sort** (por nome).
- Registrar e acompanhar pedidos via banco de dados.

---

## 🛠 Tecnologias Utilizadas

- **Python 3**
- **Flask** (microframework web)
- **SQLite** (banco de dados relacional)
- **HTML5 / CSS3**
- **Bootstrap** (framework visual)
- **Algoritmos e Estruturas de Dados**
- **Templates com Jinja2**

---

## 📁 Estrutura do Projeto

sistemaPizzaria/ 

├── app.py                  # Arquivo principal que executa a aplicação Flask

├── database.py             # Configuração e criação das tabelas no banco de dados

├── pizzabyte.db            # Banco de dados SQLite

├── static/css/             # Arquivos CSS do Bootstrap e estilos customizados

├── static/img/             # Imagens da aplicação (logos, pizzas, etc)

├── templates/              # Páginas HTML com Jinja2

├── home.html

├── cardapio.html

├── carrinho.html

├── cadastro.html

├── login.html

├── pedido.html

├── pedidomanual.html

├── relatorios.html

├── verpedido.html

├── relatorio.html

└── design/                 # Imagens do protótipo e telas do sistema

---

## 📁 Link do Projeto

https://www.mediafire.com/file/mj6lihuai1ggxqc/sistemaPizzaria.zip/file

---

## 🌐 Descrição das Páginas (na pasta `templates/`)

### 🏠 home.html
- Página inicial com banner de boas-vindas.
- Explica o processo de fazer um pedido em 3 etapas simples.
- Navegação para todas as áreas do sistema.
- Design responsivo e atraente.

### 📋 cardapio.html
- Exibe todas as pizzas disponíveis com imagens, descrições e preços.
- Permite ordenar as pizzas por preço (Bubble Sort) ou nome (Insertion Sort).
- Botão "Adicionar" para cada pizza que envia itens ao carrinho.

### 🛒 carrinho.html
- Lista os itens adicionados.
- Ajusta quantidades e remove produtos.
- Calcula subtotal, taxa de entrega e total.
- Botão para finalizar a compra e gerar o pedido.

### 📝 cadastro.html
- Formulário para cadastro de novos clientes.
- Coleta nome, endereço, celular, email e senha.
- Integração com banco para armazenar usuários.
- Validação básica de campos.

### 🔐 login.html
- Tela de autenticação com abas para clientes e administradores.
- Proteção de rotas restritas.
- Redireciona para área adequada após login.

### 📦 pedido.html
- Visualização de todos os pedidos do usuário.
- Mostra status atual (em preparo, saiu para entrega, entregue).
- Timeline visual do progresso do pedido.
- Detalhes completos do pedido.

### 🖥️ pedidomanual.html
- Área administrativa para registro de pedidos.
- Permite seleção múltipla de pizzas.
- Informações do cliente, forma de pagamento e observações.

### 📊 relatorios.html
- Painel com métricas e estatísticas:
  - Total de pedidos.
  - Receita acumulada.
  - Média por pedido.
  - Pizza mais vendida.
- Filtro por período.

### 📋 verpedido.html
- Lista de pedidos em preparo.
- Botão para atualizar status (em preparo, saiu para entrega, entregue, cancelado).
- Modal para atualização de status.
- Botão para limpar pedidos finalizados/cancelados.

### 📄 relatorio.html
- Página simples com barra de navegação para área administrativa.
- Acesso ao relatório geral.

---

## 🧠 Funcionalidades e Lógica Implementada

### 🔁 Estruturas de Dados
- **Fila (`deque`)** para gerenciar pedidos em ordem de chegada.
- **Pilha (`list`)** para armazenar pedidos cancelados, com opção de restaurar.

### ➕ Função Recursiva
- `soma_total_recursiva` calcula o total do pedido somando os valores do carrinho.

### 🔢 Algoritmos de Ordenação
- **Bubble Sort** para ordenar pizzas por preço crescente.
- **Insertion Sort** para ordenar pizzas alfabeticamente.

---

## 📊 Banco de Dados

- O banco `pizzabyte.db` é criado automaticamente na primeira execução.
- Tabelas principais:
  - `pizzas`: id, nome, descrição, preço, imagem.
  - `carrinho`: id, pizza_id, quantidade.
  - `pedidos`: id, número do pedido, status, data, total.
- Popula pizzas exemplo automaticamente (Calabresa, Frango, Portuguesa, Bacon).

---

## 🖼️ Telas e Interface

Na pasta `/design` há imagens que representam:

- Página inicial
- Login de administrador
- Visualização do cardápio
- Carrinho de pedidos
- Pedido manual
- Acompanhamento de pedidos
- Relatórios

---

## 🚀 Como Executar o Projeto
Siga os passos abaixo para rodar o sistema localmente:

1. Clone o Repositório

gh repo clone pedrinhozx865/Projeto-PizzaByte
cd sistemaPizzaria

2. Crie e Ative um Ambiente Virtual

python3 -m venv venv
source venv/bin/activate


No Linux/macOS:

python3 -m venv venv
source venv/bin/activate

No Windows (cmd):

python -m venv venv
venv\Scripts\activate

3. Instale as Dependências

Com o ambiente virtual ativado, instale o Flask:

pip install flask

4. Configure o Banco de Dados
Se você tiver um script database.py para criar as tabelas, execute:

python database.py

5. Execute a Aplicação Flask
Rode o servidor local Flask:

 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Você deverá ver uma saída como:

 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

6. Acesse o Sistema
Abra o navegador e vá para:

http://localhost:5000

## ✅ Considerações Finais

Este projeto foi desenvolvido com o objetivo de criar um sistema simples, funcional e intuitivo para gerenciamento de pedidos de uma pizzaria. Utilizando Python com Flask, o sistema permite realizar e visualizar pedidos, gerar relatórios e gerenciar o fluxo de preparo até a entrega.

A aplicação foi estruturada com organização de templates, uso de Bootstrap para uma interface responsiva e componentes dinâmicos para melhorar a experiência do usuário.

- Este é um ótimo ponto de partida para quem deseja expandir o sistema com novas funcionalidades, como:

- Integração com banco de dados mais robusto (PostgreSQL ou MySQL),

- Login com autenticação de usuários,

- Dashboard de vendas e métricas,

- Integração com serviços de entrega.

Sinta-se à vontade para usar, estudar e aprimorar este projeto!
