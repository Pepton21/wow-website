from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from guild_app.util.validators import CharacterExists, CharacterFree, UserExists, PasswordsMatch

class RegistrationForm(Form):
    username = StringField('Username', validators=[DataRequired(), CharacterExists(), CharacterFree()])
    password = PasswordField('Password', validators=[DataRequired()])

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired(), UserExists()])
    password = PasswordField('Password', validators=[DataRequired(), PasswordsMatch()])