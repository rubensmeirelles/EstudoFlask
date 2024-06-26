from app import app, db
from flask import render_template, url_for, request, redirect

from app.models import Contato
from app.forms import ContatoForm

@app.route("/")
def homepage():
    usuario = "Rubens Meirelles"
    idade = 49
    
    context = {
        'usuario': usuario,
        'idade': idade
    }
    return render_template("index.html", context=context)

@app.route("/contato/", methods=['GET', 'POST'])
def contato():
    form = ContatoForm()
    context = {}
    
    if form.validate_on_submit():
       form.save()
       return redirect(url_for('homepage'))
        
    return render_template('contato.html', context=context, form=form)

@app.route('/contato/lista/')
def contatoLista():

    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')

    dados = Contato.query.order_by('nome')
    if pesquisa != '':
        dados = dados.filter_by(nome=pesquisa)

    context = {'dados': dados.all()}
    
    return render_template('contato_lista.html', context=context)

@app.route('/contato/<int:id>/')
def contatoDetail(id):
    obj = Contato.query.get(id)
    return render_template('contato_detail.html', obj=obj)


# FORMATO NÃO RECOMENDADO

@app.route("/contato_old/", methods=['GET', 'POST'])
def contato_old():
    context = {}
    
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa')
        context.update({'pesquisa': pesquisa})
        
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']
        
        contato = Contato(
            nome=nome,
            email=email,
            assunto=assunto,
            mensagem=mensagem
        )
    
        db.session.add(contato)
        db.session.commit()
        
    return render_template('contato_old.html', context=context)