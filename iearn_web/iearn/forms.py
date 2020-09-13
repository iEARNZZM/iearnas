from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_wtf.html5 import URLField
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from flask_ckeditor import CKEditorField
from wtforms.validators import (DataRequired, Length, ValidationError,
                                 url, Optional, Email, EqualTo)
from iearn.models import Admin

# User authentication
class LoginForm(FlaskForm):
    email = StringField('El. paštas', validators=[DataRequired(message="Prašome užpildyti laukelį."), Email()])
    password = PasswordField('Slaptažodis', validators=[DataRequired(message="Prašome užpildyti laukelį.")])
    submit = SubmitField('Prisijungti')

class RequestResetForm(FlaskForm):
    email = StringField('El. paštas',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Siųsti prašymą')

    def validate_email(self, email):
        admin = Admin.query.filter_by(email=email.data).first()
        if admin is None:
            raise ValidationError('Vartotojo su tokiu el. paštu nėra.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Naujas slaptažodis', validators=[DataRequired()])
    confirm_password = PasswordField('Patvirtinkite slaptažodį',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Pakeisti slaptažodį')

# Admin update sections forms
class UpdateAboutUsForm(FlaskForm):
    content = TextAreaField('"Apie mus" tekstas', validators=[DataRequired()])
    picture = FileField('"Apie mus" teksto nuotrauka', validators=[FileAllowed(['jpeg', 'jpg', 'png'], 'Tinka tik "jpg", "jpeg", "png" formato nuotraukos.')])
    submit = SubmitField('Atnaujinti')

class EditProjectForm(FlaskForm):
    title = StringField('Pavadinimas', validators=[DataRequired()])
    short_description = TextAreaField('Trumpasis aprasymas', validators=[DataRequired(), Length(max=140, message="Aprašymas turi būti ne daugiau kaip 140 simbolių.")])
    picture = FileField('Projekto kortelės miniatiūra/nuotrauka :', validators=[FileAllowed(['jpeg', 'jpg', 'png'], 'Tinka tik "jpg", "jpeg", "png" formato nuotraukos.')])
    
    body = CKEditorField('Body', validators=[DataRequired()])
    
    save = SubmitField('Išsaugoti')
    save2 = SubmitField('Atnaujinti')
    publish = SubmitField('Paskelbti')
    delete = SubmitField('Išstrinti')

    
class CreateTeamMemberForm(FlaskForm):
    name = StringField('Vardas ir Pavardė', validators=[DataRequired()])
    member_description = StringField('Trumpa 5/6 žodžių mintis', validators=[DataRequired()])
    profile_pic = FileField('Asmens nuotrauka', validators=[FileAllowed(['jpeg', 'jpg', 'png'], 'Tinka tik "jpg", "jpeg", "png" formato nuotraukos.')])
    save = SubmitField('Išsaugoti')
    delete = SubmitField('Išstrinti')


class MediaContactsForm(FlaskForm):
    Link1 = StringField('Instagram', validators=[DataRequired(), url(message="Turi būti nurodoma nuoroda.")])
    Link2 = StringField('Facebook', validators=[DataRequired(), url(message="Turi būti nurodoma nuoroda.")])
    Link3 = StringField('YouTube', validators=[DataRequired(), url(message="Turi būti nurodoma nuoroda.")])
    Link4 = StringField('Global "iEARN"', validators=[DataRequired(), url(message="Turi būti nurodoma nuoroda.")])

    contact1 = StringField('Instagram', validators=[DataRequired()])
    contact2 = StringField('YouTube', validators=[DataRequired()])
    contact3 = StringField('Facebook', validators=[DataRequired()])
    contact4 = StringField('Global "iEARN"', validators=[DataRequired()])

    submit = SubmitField('Išsaugoti')