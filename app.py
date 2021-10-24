# Python Module Imports
import requests
import json
import os

# Flask Module Imports
from flask import (
    Flask, 
    redirect, 
    url_for, 
    render_template, 
    request, 
    send_from_directory, 
    jsonify
)

from flask_login import (
    LoginManager,
    current_user,
    login_manager,
    login_required,
    login_user,
    logout_user
)

from flask_babel import (
    Babel
)

# Web Client Imports
from oauthlib.oauth2 import (
    WebApplicationClient
)

from oauthlib.oauth2.rfc6749.endpoints import (
    authorization
)

##############################
#       Local Imports
##############################

import config
import views
import db

##############################
#     Environment Setup
##############################

# Flask App Production Code
app = Flask(__name__)
app.config.from_pyfile('config.py')

##############################
#   Google OAUTH and Login
##############################

login_manager = LoginManager()
login_manager.init_app(app)

client = WebApplicationClient(config.GOOGLE_CLIENT_ID)

@login_manager.user_loader
def get_user(user_id):
    sqlite3_response = db.lookup_user(user_id)
    return views.User(id=sqlite3_response[0][0], username=sqlite3_response[0][2], email=sqlite3_response[0][1], profile_picture=sqlite3_response[0][4])

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

##############################
#      Web Page Routing
##############################

@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template('home.html', title='Home', user=current_user)
    else:
        return render_template('login.html', title='Login')

@app.route("/games")
def games():
    sg = db.supported_games()
    return render_template(
        'games.html', 
        title='Trading', 
        user=current_user, 
        supported_games=sg
    )
    
@app.route("/offers/<name>", methods=['GET'])
def game(name):
    game_query = db.does_game_exist(name)
    if game_query is not None:
        return render_template("offers.html", game=game_query)
    else:
        return not_found_error("test")
    

@app.route("/profile")
@login_required
def profile():
    return render_template(
        'profile.html', 
        title="Profile", 
        user=current_user
    )
    
@app.route("/profile", methods=['POST'])
@login_required
def profile_post():
    pass

def get_google_provider_cfg():
    return requests.get(config.GOOGLE_DISCOVER_URL).json()

@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"]
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    
    # prepare the request for tokens from Google
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    
    # send the token request to Google's auth API
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(config.GOOGLE_CLIENT_ID, config.GOOGLE_CLIENT_SECRET),
    )
    
    # parse the tokens we received from google
    client.parse_request_body_response(json.dumps(token_response.json()))
    
    # use the retrieved tokens to grab profile information from google
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    
    # ensure the email we received is verified already
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        user_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        username = userinfo_response.json()["given_name"]
    else:
        return "User email has not been verified on your Google account!"
    
    new_user = views.User(id=unique_id, username=username, email=user_email, profile_picture=picture)
    new_user.initialize()  # if this a new account a new record will be added to the schema, else the last_login is updated
    
    # login the user we have authenticated
    login_user(new_user)
    
    # redirect to homepage
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(505)
def internal_error(error):
    return render_template('505.html'), 505

##############################
#     AJAX Data Routing
##############################

##############################
#           Main
##############################

if __name__ == "__main__":
    
    # if we are debugging locally using http, oauth will crash the app because
    # we are running over an unsecured channel -- disable ONLY FOR LOCAL DEVELOPMENT
    if config.DEBUG:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    
    # start the application
    app.run()
    
    # allows for L11n and L10n
    babel = Babel(app)
