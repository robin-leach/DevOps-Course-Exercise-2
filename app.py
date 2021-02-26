from flask import Flask, render_template, request, redirect, url_for
import sys
import logging

from entity.http_method import HttpMethod
from views.view_model import ViewModel

from db_client.index import get_db_collection
from db_client.queries import get_all_items, mark_item_as_complete, add_new_item

date_time_format = "%Y-%m-%dT%H:%M:%S.%fZ"


def create_app():
    app = Flask(__name__)

    handler = logging.StreamHandler(sys.stdout)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

    collection = get_db_collection()

    @app.route('/')
    def index():
        items = get_all_items(collection)
        return render_template('index.html', view_model=ViewModel(items))

    @app.route('/items/<id>/complete')
    def complete_item(id):
        mark_item_as_complete(collection, id)
        return redirect(url_for('index'))

    @app.route('/items/new', methods=[HttpMethod.Post.value])
    def add_item():
        name = request.form['title']
        add_new_item(collection, name)
        return redirect(url_for('index'))

    if __name__ == '__main__':
        app.run(debug=True)

    return app
