from flask import Flask, render_template, request, redirect, session, flash, url_for
from urllib.parse import quote as url_quote

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome=nome
        self.categoria=categoria
        self.console=console

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Rack n Slash', 'PS2')
jogos = [jogo1,jogo2]

usuario1 = Usuario("Denis", "DM", "teste")
usuarios = {usuario1.nickname : usuario1}

app = Flask(__name__)
app.secret_key='alura'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', lista=jogos)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuario nao logado!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogos.append(jogo)
    return redirect(url_for('index'))

app.run(debug=True)