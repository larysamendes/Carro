from flask import render_template, request, redirect, session, flash, url_for
from models import Carro

from projeto import app, db
from dao import CarroDao, UsuarioDao

carro_dao = CarroDao(db)
usuario_dao = UsuarioDao(db)

@app.route('/')
def index():
    carros = carro_dao.listar()
    print(carro_dao.listar())
    return render_template('lista.html', titulo='Carros', carros=carros)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Carro')

@app.route('/criar', methods=['POST',])
def criar():
    marca = request.form['marca']
    modelo = request.form['modelo']
    cor = request.form['cor']
    combustivel = request.form['combustivel']
    ano = request.form['ano']
    carro = Carro( marca, modelo, cor, combustivel, ano)
    carros = carro_dao.salvar(carro)
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        print(id)
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    carro = carro_dao.busca_por_id(id)
    return render_template('editar.html', titulo='Editando Carro',  carro=carro)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    marca = request.form['marca']
    modelo = request.form['modelo']
    cor = request.form['cor']
    combustivel = request.form['combustivel']
    ano = request.form['ano']
    id =  request.form['id']
    carro = Carro( marca, modelo, cor, combustivel, ano, id)
    carro_dao.salvar(carro)
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('deletar', id=id)))
    carro_dao.deletar(id)
    flash('O carro foi removido!')
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Login', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = usuario_dao.autenticar(request.form['usuario'], request.form['senha'])
    if usuario:
        session['usuario_logado'] = usuario.id
        flash(usuario.nome  +  ' fez login com sucesso')
        proxima_pagina = request.form['proxima']
        return redirect((proxima_pagina))

    else:
        flash('Usuario ou senha incorreta, tente novamente!')
        return redirect(url_for('login'))

@app.route('/carro/<int:id>')
def carro(id):
    carros = carro_dao.busca_por_id(id)
    print(carros)
    return render_template('exibir.html', titulo='Carro', carro=carros)

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash( 'Nenhum usuario logado')
    return redirect(url_for('index'))
