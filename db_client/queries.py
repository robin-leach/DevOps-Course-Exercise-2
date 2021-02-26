from bson.objectid import ObjectId
from datetime import datetime

from entity.status import Status
from entity.item import Item

date_time_format = "%Y-%m-%dT%H:%M:%S.%fZ"


def get_all_items(collection):
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
    return items


def mark_item_as_complete(collection, id):
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
    collection.insert_one(
        {
            "name": name,
            "status": Status.ToDo.value,
            "dateLastActivity": datetime.now().strftime(date_time_format)
        }
    )
