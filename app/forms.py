from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class Q1_Form(FlaskForm):
    valg = StringField('valg', validators=[DataRequired()])
    submit = SubmitField('svar')

class Q2_Form(FlaskForm):
    valg = StringField('valg', validators=[DataRequired()])
    submit = SubmitField('svar')

class Q3_Form(FlaskForm):
    submit = SubmitField('Svar_button')    

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')