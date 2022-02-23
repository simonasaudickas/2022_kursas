from flask import Flask, request, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from dictionary import data
import json
from pizza_sales import picos_pardavimai
from datetime import date
from forms import RegistracijosForma, PrisijungimoForma, ContactForm, RasytiStraipsni
from flask_login import LoginManager, UserMixin, current_user, logout_user,login_user, login_required
from flask_bcrypt import Bcrypt
import os
#import duomenu_agregavimas

app= Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'MLXH243GssUWwKdTWS7FDhdwYF56wPj8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'puslapiui.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'registruotis'
login_manager.login_message_category= 'info'


class Vartotojas(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key= True)
    vardas = db.Column("Vardas", db.String(20), unique=True, nullable=False)
    el_pastas =db.Column("El.pastas", db.String(120), unique=False, nullable=False)
    slaptazodis = db.Column("slaptazodis", db.String(60), unique=True, nullable=False)

class Straipsniai(db.Model):
    __tablename__ = 'straipsniai'
    id = db.Column(db.Integer, primary_key= True)
    autorius = db.Column("Autorius", db.String(20), unique=False, nullable=False)
    pavadinimas =db.Column("Pavadinimas", db.String(200), unique=True, nullable=False)
    straipsnis = db.Column("Straipsnis", db.String(3000), unique=True, nullable=False)
    dt = db.Column('publikuota',db.Date, nullable=False)


@login_manager.user_loader
def load_user(vartotojo_id):
    return Vartotojas.query.get(int(vartotojo_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistracijosForma()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.slaptazodis.data).decode('utf-8')
        vartotojas = Vartotojas(vardas=form.vardas.data, el_pastas = form.el_pastas.data, slaptazodis = hashed_pwd)
        db.session.add(vartotojas)
        db.session.commit()
        flash("sekmingai prisiregistravote. Galite prisijungti", 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title = 'Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form= PrisijungimoForma()
    if form.validate_on_submit():
        vartotojas = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
        if vartotojas and bcrypt.check_password_hash(vartotojas.slaptazodis, form.slaptazodis.data):
            login_user(vartotojas, remember=form.prisiminti.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Prisijungimas nepavyko. Patikrinkite varda ar el.pasta','danger')
    return render_template('login.html', form=form, title='Prisijungti')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/profile', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('profile.html')




@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('article.html', data=data)

@app.route('/<string:title>')
def article(title):
    return render_template('single_article.html', title=title, data=data)

@app.route('/add_article', methods=['GET','POST'])
@login_required
def add_article():
    db.create_all()
    form = RasytiStraipsni()
    if form.validate_on_submit():
        straipsnis = Straipsniai(autorius=form.autorius.data, pavadinimas = form.pavadinimas.data, straipsnis =form.straipsnis.data, dt=date.today())
        db.session.add(straipsnis)
        db.session.commit()
        flash("Sekmingai irasete straipsni.", 'success')
        return redirect(url_for('index'))
    return render_template("add_article.html", form=form)


@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    form = ContactForm()
    if form.validate_on_submit():
        return render_template('contact_success.html', form=form)
    return render_template('contact.html', form=form)



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pizza_sales')
def pizza_sales():
    labels = [row[0] for row in picos_pardavimai]
    values = [row[1] for row in picos_pardavimai]
    return render_template('pizza_sales_stats.html', labels=labels, values=values)


"""
@app.route('/about/'+vardas+'-'+pavarde)
def useris():
    return render_template('user.html')
"""


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
    db.create_all()