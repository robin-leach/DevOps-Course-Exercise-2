from bson.objectid import ObjectId
from datetime import datetime
import logging
from html import escape

from entity.status import Status
from entity.item import Item

date_time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
log = logging.getLogger('app')


def get_all_items(collection):
    log.debug(f'Fetching all items')
    items = []
    for item in collection.find():
        items.append(
            Item(
                item['_id'],
                item['name'],
                item['status'],
                item['dateLastActivity']
            )
        )
    log.debug(f'Found {len(items)} items')
    return items


def mark_item_as_complete(collection, id):
    log.debug(f'Marking item with ID "{escape(id)}" as complete')
    collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "status": Status.Done.value,
                "dateLastActivity":  datetime.now().strftime(date_time_format)
            }
        }
    )


def add_new_item(collection, name):
    log.debug(f'Adding item with name "{escape(name)}"')
    collection.insert_one(
        {
            "name": name,
            "status": Status.ToDo.value,
            "dateLastActivity": datetime.now().strftime(date_time_format)
        }
    )
