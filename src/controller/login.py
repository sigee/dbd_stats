import google.auth.transport.requests
import json
import os
import requests

from decorators import already_logged_in
from flask import render_template, session, redirect, request, abort, url_for
from flask.views import MethodView
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_CONFIG = json.loads(os.environ.get('GOOGLE_CLIENT_CONFIG'))

flow = Flow.from_client_config(
    client_config=GOOGLE_CLIENT_CONFIG,
    scopes=[
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email',
        'openid'
    ],
    redirect_uri='http://127.0.0.1:5000/callback'
)


class Login(MethodView):
    @already_logged_in
    def get(self):
        return render_template('login.html')


class LoginWithGoogle(MethodView):
    def get(self):
        authorization_url, state = flow.authorization_url()
        session["state"] = state
        return redirect(authorization_url)


class Callback(MethodView):
    def get(self):
        flow.fetch_token(authorization_response=request.url)

        if not session["state"] == request.args["state"]:
            abort(500)

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID
        )

        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        session["picture"] = id_info.get("picture")

        '''
        {
            'iss': 'https://accounts.google.com',
            'azp': '79614008464-n82dqas37unqpgf3vnnp89s1ah41dggi.apps.googleusercontent.com',
            'aud': '79614008464-n82dqas37unqpgf3vnnp89s1ah41dggi.apps.googleusercontent.com',
            'sub': '116716649661883837355',
            'email': 'sigee15@gmail.com',
            'email_verified': True,
            'at_hash': 't6tQRx4dwDMM4YRnLK-ZjQ',
            'name': 'Dávid Szigecsán',
            'picture': 'https://lh3.googleusercontent.com/a-/AFdZucqu8zS9OD551p44eYvw_6RgpKO4SC6dE0wv8zbkMA=s96-c',
            'given_name': 'Dávid',
            'family_name': 'Szigecsán',
            'locale': 'hu',
            'iat': 1661880771,
            'exp': 1661884371
        }
        '''

        return redirect(url_for('dashboard'))


class Logout(MethodView):
    def get(self):
        session.clear()
        return redirect(url_for('login'))
