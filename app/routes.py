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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/add_card', methods=['GET', 'POST'])
@login_required
def add_card():
    form = CardForm()
    if form.validate_on_submit():
        card = Card(word=form.word.data, translation=form.translation.data, owner=current_user)
        db.session.add(card)
        db.session.commit()
        flash('Card added successfully!')
        return redirect(url_for('cards'))
    return render_template('add_card.html', title='Add Card', form=form)

@app.route('/cards')
@login_required
def cards():
    page = request.args.get('page', 1, type=int)
    cards_pagination = current_user.cards.order_by(Card.id.desc()).paginate(page=page, per_page=10)
    next_url = url_for('cards', page=cards_pagination.next_num) if cards_pagination.has_next else None
    prev_url = url_for('cards', page=cards_pagination.prev_num) if cards_pagination.has_prev else None
    return render_template('cards.html', title='Your Cards', cards=cards_pagination.items, next_url=next_url, prev_url=prev_url)
