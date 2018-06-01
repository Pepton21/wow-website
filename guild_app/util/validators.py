from wtforms.validators import ValidationError
import requests
from guild_app.util import wowAPI
from guild_app import database as db

class CharacterExists(object):
    def __init__(self, message = 'Character not found!'):
        self.message = message
    def __call__(self, form, field):
        data = field.data.split('-')
        if len(data) != 2:
            raise ValidationError(self.message)
        name = data[0]
        realm = data[1]
        request = requests.get(url="{}character/{}/{}?locale=en_GB&apikey={}".format(wowAPI.base_uri, realm, name, wowAPI.key))
        if request.status_code != 200:
            raise ValidationError(self.message)

class CharacterFree(object):
    def __init__(self, message = 'Character name taken!'):
        self.message = message
    def __call__(self, form, field):
        cnx = db.get_connection()
        cursor = cnx.cursor()
        cursor.execute(("SELECT ID FROM Users WHERE Username = %s"), (field,))
        if cursor.rowcount != 0:
            cursor.close()
            cnx.close()
            raise ValidationError(self.message)
        cursor.close()
        cnx.close()

class PasswordMatch(object):
    def __init__(self, message = 'Incorrect password!'):
        self.message = message
    def __call__(self, form, field):
        data = field.split('-')
        if len(data) != 2:
            raise ValidationError(self.message)
        name = data[0]
        realm = data[1]
        request = requests.get(url="{}characters/{}/{}?locale=en_GB&apikey={}".format(wowAPI.base_uri, realm, name, wowAPI.key))
        if request.status_code != 200:
            raise ValidationError(self.message)