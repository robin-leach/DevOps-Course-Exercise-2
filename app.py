from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user, current_user
from oauthlib.oauth2 import WebApplicationClient
import sys
import logging
import requests
import os
from html import escape

from db_client.index import get_db_collection
from db_client.queries import get_all_items, mark_item_as_complete, add_new_item
from decorators.require_write_privilege import require_write_privilege
from helpers.index import generate_random_string
from entity.http_method import HttpMethod
from entity.user import User
from entity.user_role import UserRole
from views.view_model import ViewModel


date_time_format = "%Y-%m-%dT%H:%M:%S.%fZ"


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    login_disabled = os.getenv('LOGIN_DISABLED').upper() == 'TRUE'
    app.config['LOGIN_DISABLED'] = login_disabled

    handler = logging.StreamHandler(sys.stdout)
    app.logger.addHandler(handler)
    app.logger.setLevel(os.getenv('LOG_LEVEL'))
    log = logging.getLogger('app')

    collection = get_db_collection()

    login_manager = LoginManager()

    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    state = generate_random_string(6)

    oauth_client = WebApplicationClient(client_id)

    log.info('App has initiliased')

    @login_manager.unauthorized_handler
    def unauthenticated():
        log.debug('Redirecting user to authenticator')

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
        log.debug('User has hit login callback')

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

        log.debug(f'Logging in user with username "{escape(github_username)}"')

        user = User(github_username)
        login_success = login_user(user)

        if login_success:
            log.debug(f'User login for "{escape(github_username)}" successful')
            return redirect(url_for('index'))
        else:
            log.error(f'User login for "{escape(github_username)}" unsuccessful')
            return "Unauthorised", 403

    @app.route('/')
    @login_required
    def index():
        user: User = current_user
        readonly = (
            not login_disabled) and user.get_role() == UserRole.Reader

        items = get_all_items(collection)

        return render_template('index.html', view_model=ViewModel(items, readonly))

    @app.route('/items/<id>/complete')
    @require_write_privilege
    @login_required
    def complete_item(id):
        log.debug(
            f'Recieved request to mark item with ID "{escape(id)}" as complete')

        mark_item_as_complete(collection, id)

        log.debug(f'Item with ID "{escape(id)}" marked as complete')
        return redirect(url_for('index'))

    @app.route('/items/new', methods=[HttpMethod.Post.value])
    @require_write_privilege
    @login_required
    def add_item():
        name = request.form['title']
        log.debug(f'Recieved add item request for item "{escape(name)}"')

        add_new_item(collection, name)

        log.debug(f'Item with name "{escape(name)}" added')
        return redirect(url_for('index'))

    if __name__ == '__main__':
        app.run(debug=True)

    return app
