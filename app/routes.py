from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms import EditProfileForm, LoginForm, RegistrationForm
from app.models import User


#Definindo as rotas. 
@app.route('/')
@app.route('/index')
@login_required # pretege as páginas de pessoas logadas como anonimo ou sem estar logado
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day int Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('index')) #verificando se está logado ou não 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():   #faz logout do perfil. 
    logout_user()
    return redirect(url_for('index'))

# Verifica se o usuario não está logado, e logo registra e add no banco de dados.
@app.route('/register', methods=['GET', 'POST']) 
def register(): 
    if current_user.is_authenticated: 
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit(): 
        user = User(username=form.username.data, email=form.email.data)   
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username): #Procura o usuário no banco de dados se não tiver, aciona o erro 404 para o usuário.
    user = User.query.filter_by(username=username).first_or_404() 
    posts = [
        {'author': user, 'body': 'Test post #1'},       
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():   #Editar função de visualização do perfil. 
    if current_user.is_authenticated: 
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
@app.route('/editprofile', methods=['GET', 'POST'])
@login_required 
def edit_profile(): 
    form = EditProfileForm() 
    if form.validate_on_submit(): 
        current_user.username = form.username.data 
        current_user.about_me = form.about_me.data 
        db.session.commit() 
        flash('You changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET': 
        form.username.data = current_user.username 
        form.about_me.data = current_user.about_me 
    return render_template('edit_profile.html', title='Edit Profile', form=form)