from flask import Flask, render_template, request, redirect, url_for
import sys
import logging

from entity.http_method import HttpMethod
from entity.list_name import ListName

from trello_requests.trello_requests import get_items_on_board, get_lists_on_board, update_item_list, create_item
from helpers.index import get_id_of_list, map_trello_items

app = Flask(__name__)

handler = logging.StreamHandler(sys.stdout)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

@app.route('/')
def index():
    trello_lists = get_lists_on_board()
    trello_items = get_items_on_board()
    
    items = map_trello_items(trello_lists, trello_items)
    return render_template('index.html', items = items)

@app.route('/items/<id>/complete')
def complete_item(id):
    done_list_id = get_id_of_list(ListName.Done.value)
    update_item_list(id, done_list_id)
    return redirect(url_for('index')) 

@app.route('/items/new', methods=[HttpMethod.Post.value])
def add_item():
    title = request.form['title']
    to_do_list_id = get_id_of_list(ListName.ToDo.value)
    create_item(title, to_do_list_id)
    return redirect(url_for('index')) 

if __name__ == '__main__':
    app.run()