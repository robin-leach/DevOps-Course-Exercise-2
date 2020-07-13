import consts
from trello_requests.make_trello_request import make_trello_request
from trello_requests.helpers import extract_trello_items, extract_trello_lists
from entity.http_method import HttpMethod

def get_lists_on_board():
    endpoint = f'{consts.trello_base_url}/boards/{consts.trello_board_id}/lists'
    params = { 'key': consts.trello_key, 'token': consts.trello_token }
    method = HttpMethod.Get
    
    response = make_trello_request(method, endpoint, params)
    return list(map(extract_trello_lists,response.json()))

def get_items_on_board():
    endpoint = f'{consts.trello_base_url}/boards/{consts.trello_board_id}/cards'
    params = { 'key': consts.trello_key, 'token': consts.trello_token }
    method = HttpMethod.Get

    response = make_trello_request(method, endpoint, params)
    return list(map(extract_trello_items,response.json()))

def update_item_list(item_id, list_id):
    endpoint = f'{consts.trello_base_url}/cards/{item_id}'
    params = { 'key': consts.trello_key, 'token': consts.trello_token, 'idList': list_id}
    method = HttpMethod.Put

    make_trello_request(method, endpoint, params)

def create_item(item_name, list_id):
    endpoint = f'{consts.trello_base_url}/cards'
    params = { 'key': consts.trello_key, 'token': consts.trello_token, 'name': item_name, 'idList': list_id}
    method = HttpMethod.Post

    make_trello_request(method, endpoint, params)