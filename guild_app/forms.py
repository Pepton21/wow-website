from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from guild_app.util.validators import CharacterExists

class RegistrationForm(Form):
    username = StringField('Username', validators=[DataRequired(), CharacterExists()])
    password = PasswordField('Password', validators=[DataRequired()])