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

if __name__ == '__main__':
    app.run(debug=True)