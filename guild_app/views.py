from guild_app import app
from guild_app.util import wowAPI
from guild_app.util import tabard_info
from flask import render_template, request as flask_request, redirect, session as flask_session
import urllib.request as urllib_request
import json
import base64
import hashlib
from random import choice
from string import ascii_uppercase
import requests
import datetime
import guild_app.forms as forms
from guild_app import database as db

@app.context_processor
def inject_tabard():
    return dict(tabard=tabard_info.tabard)

@app.route("/")
@app.route("/index")
def home():
    result = {}
    request = requests.get(url=wowAPI.guild_info_uri + wowAPI.key)
    content = json.loads(request.text)
    result['guild_info'] = content
    request = requests.get(url=wowAPI.guild_members_uri + wowAPI.key)
    content = json.loads(request.text)
    result['guild_members'] = content
    print(result)
    class_dist = {'Warrior': 0, 'Paladin': 0, 'Hunter': 0, 'Rogue': 0, 'Priest': 0, 'Death Knight': 0, 'Shaman': 0,
                  'Mage': 0, 'Warlock': 0, 'Monk': 0, 'Druid': 0, 'Demon Hunter': 0}
    for member in result['guild_members']['members']:
        class_dist[wowAPI.class_map[member['character']['class']]] += 1
    result['class_dist'] = class_dist
    request = requests.get(url="https://www.wowprogress.com/guild/eu/arathor/The+Forgotten+Few/json_rank")
    content = json.loads(request.text)
    result['wowprogress'] = content
    result['class_colors'] = wowAPI.class_colors
    print(result)
    return render_template('index.html', result=result)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        salt = ''.join(choice(ascii_uppercase) for i in range(10))
        t_sha = hashlib.sha512()
        t_sha.update((form.password.data + salt).encode('utf-8'))
        hashed_password = base64.urlsafe_b64encode(t_sha.digest())
        cnx = db.get_connection()
        cursor = cnx.cursor()
        name, realm = form.username.data.split('-')
        user_data = {'username': form.username.data, 'password': hashed_password, 'salt': salt, 'role': 1}
        cursor.execute((
            "INSERT INTO Users (Username, PasswordHash, Salt, Role) VALUES (%(username)s, %(password)s, %(salt)s, %(role)s)"),
            user_data)
        character_data = {'name': name, 'realm': realm}
        cursor.execute((
            "INSERT INTO Characters (Name, Realm) VALUES (%(name)s, %(realm)s)"),
            character_data)
        cnx.commit()
        cursor.execute(("SELECT ID FROM Users WHERE Username = %s"), (form.username.data,))
        user_id = cursor.fetchone()[0]
        cursor.execute(("SELECT ID FROM Characters WHERE Name = %s AND Realm = %s"), (name, realm))
        character_id = cursor.fetchone()[0]
        cursor.execute(("UPDATE Users SET MainChar = %s WHERE ID = %s"), (character_id, user_id))
        cursor.execute(("UPDATE Characters SET UserID = %s WHERE ID = %s"), (user_id, character_id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return redirect("/index")
    return render_template('register.html', form=form)

@app.route("/logout")
def logout():
    flask_session.clear()
    return redirect("index")

@app.route("/members")
def members():
    result = {}
    request = requests.get(url=wowAPI.guild_members_uri + wowAPI.key)
    content = json.loads(request.text)
    result['guild_members'] = content
    for member in result['guild_members']['members']:
        member['character']['race_name'] = wowAPI.race_map[member['character']['race']]
        member['character']['class_name'] = wowAPI.class_map[member['character']['class']]
    result['class_colors'] = wowAPI.class_alternate_colors
    return render_template('members.html', result=result)

@app.route("/member")
def member():
    realm = flask_request.args.get('realm')
    name = flask_request.args.get('name')
    result = {}
    print("{}character/{}/{}?fields=items&locale=en_GB&apikey={}".format(wowAPI.base_uri, realm, name, wowAPI.key))
    print(tabard_info.tabard)
    request = requests.get(url="{}character/{}/{}?fields=items&locale=en_GB&apikey={}".format(wowAPI.base_uri, realm, name, wowAPI.key))
    content = json.loads(request.text)
    result['guild_member'] = content
    result['class_colors'] = wowAPI.class_alternate_colors
    result['class_map'] = wowAPI.class_map
    result['race_map'] = wowAPI.race_map
    print(result)
    return render_template('member.html', result=result)

@app.route("/news")
def news():
    request = requests.get(url=wowAPI.guild_news_uri + wowAPI.key)
    result = {}
    if request.status_code == 200:
        content = json.loads(request.text)
        print(content)
        for record in content['news']:
            record['timestamp'] = datetime.datetime.fromtimestamp(record['timestamp'] / 1e3)
        result = {}
        result['news'] = content['news']
    else:
        result['news'] = None
    return render_template('news.html', result=result)

@app.route("/tabard")
def tabard():
    return render_template("tabard.html")

@app.route("/refresh-tabard")
def refresh_tabard():
    request = requests.get(url=wowAPI.guild_info_uri + wowAPI.key)
    content = json.loads(request.text)
    tabard = {'emblem': content['emblem']['icon'], 'border': content['emblem']['border'], 'icon color': content['emblem']['iconColorId'], 'bg color': content['emblem']['backgroundColorId'], 'border color': content['emblem']['borderColorId'],
          'faction': 'Alliance'}
    cnx = db.get_connection()
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM GuildTabard")
    cursor.execute(("INSERT INTO GuildTabard (Icon, Border, IconColor, BgColor, BorderColor, faction) VALUES (%(emblem)s, %(border)s, %(icon color)s, %(bg color)s, %(border color)s, %(faction)s)"), tabard)
    cnx.commit()
    cursor.close()
    emblem = str(content['emblem']['icon']).zfill(2) if content['emblem']['icon'] < 10 else content['emblem']['icon']
    border = str(content['emblem']['border']).zfill(2) if content['emblem']['border'] < 10 else content['emblem']['border']
    urllib_request.urlretrieve("{}emblem_{}.png".format(wowAPI.tabard_uri, emblem), "guild_app/static/images/guild/tabards/emblem_{}.png".format(emblem))
    urllib_request.urlretrieve("{}border_{}.png".format(wowAPI.tabard_uri, border), "guild_app/static/images/guild/tabards/border_{}.png".format(border))
    return redirect("/tabard")
