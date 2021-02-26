from datetime import datetime
import random
import string

from entity.item import Item

date_time_format = "%Y-%m-%dT%H:%M:%S.%fZ"


def start_of_day(day):
    return day.replace(hour=0, minute=0, second=0, microsecond=0)


def filter_items_by_list(items, list_name):
    filtered_items = []
    for item in items:
        if(item.status == list_name):
            filtered_items.append(item)
    return filtered_items


def filter_items_modified_today(items):
    start_of_today = start_of_day(datetime.now())

    filtered_items = []

    for item in items:
        modified_time = datetime.strptime(
            item.last_modified_date,
            date_time_format
        )
        modified_date = start_of_day(modified_time)

        if(start_of_today == modified_date):
            filtered_items.append(item)

    return filtered_items


def filter_items_last_modified_before_today(items):
    start_of_today = start_of_day(datetime.now())

    filtered_items = []

    for item in items:
        modified_time = datetime.strptime(
            item.last_modified_date,
            date_time_format
        )

        if(modified_time < start_of_today):
            filtered_items.append(item)

    return filtered_items
