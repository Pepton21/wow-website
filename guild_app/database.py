import mysql.connector
import os

from guild_app.util import crypto

DATABASE = "crimsonmoon$default"
USER = "crimsonmoon"
HOST = "crimsonmoon.mysql.pythonanywhere-services.com"
f = open("../guild_password.txt")
PASSWORD = f.read()
f.close()

def get_connection():
    cnx = mysql.connector.connect(user=USER, password=PASSWORD,
                                  host=HOST,
                                  database=DATABASE)
    return cnx