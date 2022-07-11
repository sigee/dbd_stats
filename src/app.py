import os

from controller.login import Login, LoginWithGoogle, Callback, Logout
from controller.match import Match, Edit, Dashboard
from flask import Flask

app = Flask(__name__, static_url_path='', static_folder='static')
app.secret_key = os.environ.get('APP_SECRET_KEY', 'any random string')

app.add_url_rule('/', view_func=Dashboard.as_view('dashboard'))
app.add_url_rule('/login', view_func=Login.as_view('login'))
app.add_url_rule('/login_with_google', view_func=LoginWithGoogle.as_view('login_with_google'))
app.add_url_rule('/callback', view_func=Callback.as_view('callback'))
app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
app.add_url_rule('/match', view_func=Match.as_view('match'))
app.add_url_rule('/edit/<id>', view_func=Edit.as_view('edit'))
