from guild_app import app

# CERN Single-Sign-On
SSO_ATTRIBUTE_MAP = {
    "ADFS_LOGIN": (True, 'nickname'),
    "ADFS_EMAIL": (True, 'email'),
}

#cmdb_app.config['SSO_ATTRIBUTE_MAP'] = SSO_ATTRIBUTE_MAP

"""@SSO.login_handler
def login_callback(user_info): 
    session['user'] = user_info"""

if __name__ == "__main__":
    app.run()