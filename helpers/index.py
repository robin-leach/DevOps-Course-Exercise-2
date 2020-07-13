import logging

from entity.item import Item
from trello_requests.trello_requests import get_lists_on_board

log = logging.getLogger('app')

def map_trello_items(trello_lists, trello_items):
    items = []
    for trello_item in trello_items:
        for trello_list in trello_lists:
            if (trello_item.listId == trello_list.id):
                items.append(Item(trello_item.id, trello_item.title, trello_list.name))
                break
    return items

def get_id_of_list(name):
    log.debug(f'Getting list with name {name}')
    lists = get_lists_on_board()
    for list in lists:
        if(list.name == name):
            return list.id
    log.debug(f'No list found with name {name}')