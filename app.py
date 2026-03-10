from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sistema"
    )

@app.route('/')
def index():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conexao.close()
    return render_template("index.html", usuarios=usuarios)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['nome']
    email = request.form['email']

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", (nome, email))
    conexao.commit()
    conexao.close()

    return redirect('/')

@app.route('/excluir/<int:id>')
def excluir(id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id=%s", (id,))
    conexao.commit()
    conexao.close()

    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        conexao.close()
        
        if usuario:
            return redirect('/vendas')
        else:
            return render_template('login.html', error='Credenciais inválidas')
    return render_template('login.html')

@app.route('/vendas')
def vendas():
    # Lista de carros hardcoded para exemplo
    carros = [
        {'id': 1, 'modelo': 'Fusca', 'preco': 15000, 'imagem': 'https://via.placeholder.com/300x200?text=Fusca'},
        {'id': 2, 'modelo': 'Civic', 'preco': 50000, 'imagem': 'https://via.placeholder.com/300x200?text=Civic'},
        {'id': 3, 'modelo': 'Corolla', 'preco': 60000, 'imagem': 'https://via.placeholder.com/300x200?text=Corolla'}
    ]
    return render_template('vendas.html', carros=carros)

if __name__ == '__main__':
    app.run(debug=True)