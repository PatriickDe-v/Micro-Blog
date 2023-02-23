from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.models import User


#Formulário de login 
class LoginForm(FlaskForm): 
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

#Formulário de Cadastro 
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    

    def validate_username(self, username): # Verifica se existe o mesmo login no banco de dados.
        user = User.query.filter_by(username=username.data).first() 
        if user is not None: 
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):  # Verfica se existe o mesmo email no banco de dados
        user = User.query.filter_by(email=email.data).first()  
        if user is not None:  
            raise ValidationError('Please use a different email adress.')
