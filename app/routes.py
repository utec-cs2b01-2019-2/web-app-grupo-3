from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from app.models import User, Post
from datetime import datetime

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = current_user.user_posts()
    return render_template('user.html', user=user, posts=posts)

@app.route('/posts', methods=['GET','POST'])
@login_required
def posts():
    form=PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Enhorabuena! Haz hecho un post!')
        return redirect(url_for('posts'))
    posts = current_user.followed_posts().all()
    return render_template("posts.html", title="Escribe algo!", form=form, posts=posts)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Home")

@app.route('/cursos')
@login_required
def cursos():
    cursos=[{'nombre': 'Teoria de la Computacion'}, {'nombre':'Programacion Orientada a Objetos 1'}, {'nombre':'Intro. a Ciencia de la Computacion'}]
    return render_template('cursos.html', title='Listado de Cursos', cursos=cursos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nombre de usuario o password equivocado.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
    return render_template('login.html', title='Sing In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'] )
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, gender=form.gender.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Felicitaciones! Ahora perteneces a la comunidad de Cientificos de la Computacion en UTEC.')
        return redirect(url_for('login'))
    #Other case, when the user request the page
    return render_template('register.html', title='Register', form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Los cambios han sido guardados.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/follow/<username>') #ruta para seguir usuarios
@login_required
def follow(username): #Funcion que recibe como parametro a quien queremos seg
    user = User.query.filter_by(username=username).first() #filtra segun userna
    if user is None:
        flash('El usuario {} no ha sido encontrado.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('No puedes seguirte a ti mismo!')
        return redirect(url_for('user',username=username))
    current_user.follow(user) #funcion que se agrego antes que permite seguir
    db.session.commit()
    flash('Ahora sigues a {}'.format(username))
    return redirect(url_for('user',username=username))

@app.route('/unfollow/<username>') #ruta para dejar de seguir usuarios
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first() #filtra segun userna
    if user is None:
        flash('El usuario {} no ha sido encontrado.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('No puedes dejar de seguirte!')
        return redirect(url_for('user',username=username))
    current_user.unfollow(user) #funcion que permite dejar de seguir
    db.session.commit()
    flash('Dejaste de seguir a {}'.format(username))
    return redirect(url_for('user',username=username))

@app.route('/explore')
@login_required
def explore():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', title='Explore', posts=posts)

@app.route('/delete/<username>/')
@login_required
def delete(username):
    user = User.query.filter_by(username=username).first()
    for post in user.posts:
        posts.remove(post)
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado')
    return render_template("login.html",title='Deleted')


@app.route('/temp')
@login_required
def temp():
    return render_template('temp.html', title='Quelocura')
