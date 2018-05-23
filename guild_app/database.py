from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import MetaData
import os

from guild_app.util import crypto

DATABASE = "cmdb"
USER = "cmdb_admin"
HOST = "dbod-cmdbpgs.cern.ch"
PORT = "6609"
SECRET_PHRASE = "R4q3tAr0tOnD4"

def get_alchemy_connection_string():
    return "postgres://" + USER + ":" + get_password() + "@" + HOST + ":" + PORT + "/" + DATABASE

def get_encrypted_password():
        return os.environ['pwd']

def get_password():
    cipher = crypto.AESCipher(SECRET_PHRASE)
    encrypted = get_encrypted_password()
    return cipher.decrypt(encrypted)


Base = automap_base(metadata=MetaData(schema="it_cmdb"))

# engine, suppose it has two tables 'user' and 'address' set up
engine = create_engine(get_alchemy_connection_string())

# reflect the tables
Base.prepare(engine, reflect=True)

db_session = Session(engine)