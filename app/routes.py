from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import RegistrationForm, LoginForm, CardForm
from app.models import User, Card
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
@login_required
def index():
    if current_user.cards.count() == 0:
        flash('You have no cards yet. Let\'s add your first card!')
        return redirect(url_for('add_card'))
    return redirect(url_for('cards'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add_card', methods=['GET', 'POST'])
@login_required
def add_card():
    form = CardForm()
    if form.validate_on_submit():
        card = Card(word=form.word.data, translation=form.translation.data, owner=current_user)
        db.session.add(card)
        db.session.commit()
        flash('Your card has been added!')
        return redirect(url_for('cards'))
    return render_template('add_card.html', form=form)

@app.route('/cards')
@login_required
def cards():
    cards = current_user.cards.all()
    return render_template('cards.html', cards=cards)
