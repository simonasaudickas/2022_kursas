from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo


class ContactForm(FlaskForm):
    name = StringField("Vardas", [DataRequired(), Length(min=5, message='Vardas negali buti trumpesnis nei 5 simboliai')])
    email = StringField('El.pastas', [Email(message="Neteisingas adresas."), DataRequired()])
    body = TextAreaField('Jusu pranesimas', [DataRequired(), Length(min=20, message='Per trumpa zinute.')])
    submit = SubmitField('Siusti')

class RegistracijosForma(FlaskForm):
    vardas = StringField('Vardas', [DataRequired()])
    el_pastas = StringField('El.pastas', [DataRequired()])
    slaptazodis = PasswordField('Slaptazodis', [DataRequired()])
    patvirtintas_slaptazodis = PasswordField('Pakartoti slaptazodi',[EqualTo('slaptazodis', "Slaptazodziai turi sutapti.")])
    submit = SubmitField('Registruotis')

    def tikrinti_vartotoja(self, vardas):
        vartotojas =app.Vartotojas.query.filter_by(vardas=vardas.data).count() < 1
        if vartotojas:
            raise ValidationError ('Sis vartotojas jau uzimtas. Pasirinkite kita')

    def tikrinti_pasta(self,el_pastas):
        vartotojas = app.Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
        if vartotojas:
            raise ValidationError('Sis pastas jau uzimtas. Pasirinkite kita')

class PrisijungimoForma(FlaskForm):
    el_pastas = StringField('El. paštas', [DataRequired()])
    slaptazodis = PasswordField('Slaptažodis', [DataRequired()])
    prisiminti = BooleanField("Prisiminti mane")
    submit = SubmitField('Prisijungti')

class RasytiStraipsni(FlaskForm):
    autorius = StringField('Vardas Pavarde', [DataRequired()])
    pavadinimas = StringField('Pavadinimas', [DataRequired()])
    straipsnis = TextAreaField("Ivesti norima straipsnio teksta", [DataRequired(), Length(min=150, message='Per trumpas straipsnis.')])
    submit = SubmitField('Siusti')

class PicosUzsakymoForma(FlaskForm):
    klientas = StringField('Vardas pavarde', [DataRequired()])
    pavadinimas = StringField('Picos pavadinimas', [DataRequired()])
    telefonas = StringField('Kliento telefonas', [DataRequired()])
    vegetariska = BooleanField("vegetariska")
    pristatymas = BooleanField("Rekalingas pristatymas")
    komentaras = TextAreaField("Irasykite komentara")
    submit = SubmitField('Uzsakyti')

class VideoUploadForma(FlaskForm):
    pasirinkimo_variantai = ["muzika", "programavimas", "kita"]
    code = StringField("Kodas", [DataRequired()])
    video_tipai = SelectField(u'Pasirinkti', choices=pasirinkimo_variantai, validators=[DataRequired()])
    submit = SubmitField('Irasyti')