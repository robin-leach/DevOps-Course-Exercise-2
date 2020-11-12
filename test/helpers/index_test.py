import pytest
from datetime import datetime, timedelta
from freezegun import freeze_time

from entity.list_name import ListName
from entity.item import Item

from helpers.index import filter_items_by_list, filter_items_modified_today, filter_items_last_modified_before_today, filter_items_last_modified_before_today


@pytest.fixture
def to_do_item():
    item = Item(
        'to-do-id',
        'to-do-title',
        ListName.ToDo.value,
        "2020-06-24T14:51:12.321Z"
    )
    return item


@pytest.fixture
def doing_item():
    item = Item(
        'doing-id',
        'doing-title',
        ListName.Doing.value,
        "2020-06-24T14:51:12.321Z"
    )
    return item


@pytest.fixture
def done_item():
    item = Item(
        'done-id',
        'done-title',
        ListName.Done.value,
        "2020-06-24T14:51:12.321Z"
    )
    return item


def test_filter_items_picks_out_to_do_items(to_do_item, doing_item, done_item):
    unfiltered_list = [to_do_item, doing_item, done_item]

    filtered_items = filter_items_by_list(unfiltered_list, ListName.ToDo.value)

    assert len(filtered_items) == 1
    assert filtered_items[0].title == to_do_item.title


def test_filter_items_handles_multiple_to_do_items(to_do_item, doing_item, done_item):
    unfiltered_list = [to_do_item, doing_item, to_do_item, done_item]

    filtered_items = filter_items_by_list(unfiltered_list, ListName.ToDo.value)

    assert len(filtered_items) == 2
    assert filtered_items[0].title == to_do_item.title
    assert filtered_items[1].title == to_do_item.title


def test_filter_items_handles_no_to_do_items(to_do_item, doing_item, done_item):
    unfiltered_list = [doing_item, done_item]

    filtered_items = filter_items_by_list(unfiltered_list, ListName.ToDo.value)

    assert len(filtered_items) == 0


def test_filter_items_handles_empty_items(to_do_item, doing_item, done_item):
    unfiltered_list = []

    filtered_items = filter_items_by_list(unfiltered_list, ListName.ToDo.value)

    assert len(filtered_items) == 0


@freeze_time("2020-06-25")
def test_filter_items_modified_today_picks_out_items_from_that_day():
    unfiltered_list = [
        Item(
            'yesterday-item',
            'yesterday-title',
            ListName.Done.value,
            "2020-06-24T14:51:12.321Z"
        ),
        Item(
            'today-item',
            'today-title',
            ListName.Done.value,
            "2020-06-25T14:51:12.321Z"
        ),
        Item(
            'tomorrow-item',
            'tomorrow-title',
            ListName.Done.value,
            "2020-06-26T14:51:12.321Z"
        )
    ]

    filtered_items = filter_items_modified_today(unfiltered_list)

    assert len(filtered_items) == 1
    assert filtered_items[0].id == 'today-item'


@freeze_time("2020-06-25")
def test_filter_items_last_modified_before_today_picks_out_items_from_before_that_day():
    unfiltered_list = [
        Item(
            'yesterday-item',
            'yesterday-title',
            ListName.Done.value,
            "2020-06-24T14:51:12.321Z"
        ),
        Item(
            'today-item',
            'today-title',
            ListName.Done.value,
            "2020-06-25T14:51:12.321Z"
        ),
        Item(
            'tomorrow-item',
            'tomorrow-title',
            ListName.Done.value,
            "2020-06-26T14:51:12.321Z"
        )
    ]

    filtered_items = filter_items_last_modified_before_today(unfiltered_list)

    assert len(filtered_items) == 1
    assert filtered_items[0].id == 'yesterday-item'
