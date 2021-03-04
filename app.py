from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user
from oauthlib.oauth2 import WebApplicationClient
import sys
import logging
import requests
import os

from entity.http_method import HttpMethod
from entity.user import User
from views.view_model import ViewModel
from helpers.index import generate_random_string

from db_client.index import get_db_collection
from db_client.queries import get_all_items, mark_item_as_complete, add_new_item

date_time_format = "%Y-%m-%dT%H:%M:%S.%fZ"


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED')

    handler = logging.StreamHandler(sys.stdout)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    log = logging.getLogger('app')

    collection = get_db_collection()

    login_manager = LoginManager()

    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    state = generate_random_string(6)

    oauth_client = WebApplicationClient(client_id)

    @login_manager.unauthorized_handler
    def unauthenticated():
        request_uri = oauth_client.prepare_request_uri(
            "https://github.com/login/oauth/authorize",
            state=state
        )
        return redirect(request_uri)

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app)

    @app.route("/login/callback", methods=["GET"])
    def callback():
        token_request_url, token_request_headers, token_request_body = oauth_client.prepare_token_request(
            token_url="https://github.com/login/oauth/access_token",
            authorization_response=request.url,
            state=state,
            client_secret=client_secret
        )
        token_response = requests.post(
            token_request_url,
            headers=token_request_headers,
            data=token_request_body
        )
        oauth_client.parse_request_body_response(
            token_response.content.decode(),
            state=state
        )

        user_info_request_url, user_info_request_headers, user_info_request_body = oauth_client.add_token(
            uri='https://api.github.com/user',
        )
        user_info_response = requests.get(
            user_info_request_url,
            data=user_info_request_body,
            headers=user_info_request_headers
        )

        github_username = user_info_response.json()['login']
        user = User(github_username)
        login_success = login_user(user)

        if login_success:
            return redirect(url_for('index'))

    @app.route('/')
    @login_required
    def index():
        items = get_all_items(collection)
        return render_template('index.html', view_model=ViewModel(items))

    @app.route('/items/<id>/complete')
    @login_required
    def complete_item(id):
        mark_item_as_complete(collection, id)
        return redirect(url_for('index'))

    @app.route('/items/new', methods=[HttpMethod.Post.value])
    @login_required
    def add_item():
        name = request.form['title']
        add_new_item(collection, name)
        return redirect(url_for('index'))

    if __name__ == '__main__':
        app.run(debug=True)

    return app
