from wtforms.validators import ValidationError
import requests
from guild_app.util import wowAPI
from guild_app import database as db
import hashlib
import base64

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

class UserExists(object):
    def __init__(self, message = 'Username not found!'):
        self.message = message
    def __call__(self, form, field):
        cnx = db.get_connection()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(("SELECT ID FROM Users WHERE Username = %s"), (field.data,))
        if cursor.rowcount != 0:
            cursor.close()
            cnx.close()
            raise ValidationError(self.message)
        cursor.close()
        cnx.close()

class PasswordsMatch(object):
    def __init__(self, message = 'Username not found!'):
        self.message = message
    def __call__(self, form, field):
        cnx = db.get_connection()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(("SELECT PasswordHash, Salt FROM Users WHERE Username = %s"), (field.data,))
        result = cursor.fetchone()
        hash = result[0]
        salt = result[1]
        t_sha = hashlib.sha512()
        t_sha.update((field.data + salt).encode('utf-8'))
        hashed_password = base64.urlsafe_b64encode(t_sha.digest())
        if hash != hashed_password:
            cursor.close()
            cnx.close()
            raise ValidationError(self.message)
        cursor.close()
        cnx.close()

class CharacterFree(object):
    def __init__(self, message = 'Character name taken!'):
        self.message = message
    def __call__(self, form, field):
        cnx = db.get_connection()
        cursor = cnx.cursor(buffered=True)
        data = field.data.split('-')
        if len(data) != 2:
            raise ValidationError(self.message)
        name = data[0]
        realm = data[1]
        cursor.execute(("SELECT ID FROM Characters WHERE Name = %s AND Realm = %s"), (name, realm))
        if cursor.rowcount != 0:
            cursor.close()
            cnx.close()
            raise ValidationError(self.message)
        cursor.close()
        cnx.close()