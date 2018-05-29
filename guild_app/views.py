from guild_app import app
from guild_app.util import wowAPI
from guild_app.util import tabard_info
from flask import render_template, request as flask_request, redirect
import json
import requests
import datetime

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

@app.route("/members")
def members():
    result = {}
    request = requests.get(url=wowAPI.guild_members_uri + wowAPI.key)
    content = json.loads(request.text)
    result['guild_members'] = content
    for member in result['guild_members']['members']:
        member['character']['race'] = wowAPI.race_map[member['character']['race']]
        member['character']['class'] = wowAPI.class_map[member['character']['class']]
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
    print(content)
    return content
    return redirect("/tabard")
