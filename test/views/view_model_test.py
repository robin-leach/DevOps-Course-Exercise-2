import pytest

from entity.list_name import ListName
from entity.item import Item
from views.view_model import ViewModel


@pytest.fixture
def to_do_item():
    return Item('to-do-id', 'to-do-title', ListName.ToDo.value, "2020-06-24T14:51:12.321Z")


@pytest.fixture
def doing_item():
    return Item('doing-id', 'doing-title', ListName.Doing.value, "2020-06-24T14:51:12.321Z")


@pytest.fixture
def done_item():
    return Item('done-id', 'done-title', ListName.Done.value, "2020-06-24T14:51:12.321Z")


@pytest.fixture
def view_model():
    return ViewModel(
        [
            Item('to-do-id', 'to-do-title', ListName.ToDo.value,
                 "2020-06-24T14:51:12.321Z"),
            Item('doing-id', 'doing-title', ListName.Doing.value,
                 "2020-06-24T14:51:12.321Z"),
            Item('done-id', 'done-title', ListName.Done.value,
                 "2020-06-24T14:51:12.321Z")
        ]
    )


def test_to_do_items_returns_items_in_to_do_column(view_model):
    assert len(view_model.to_do_items) == 1
    assert view_model.to_do_items[0].title == 'to-do-title'


def test_doing_items_returns_items_in_doing_column(view_model):
    assert len(view_model.doing_items) == 1
    assert view_model.doing_items[0].title == 'doing-title'


def test_done_returns_items_in_done_column(view_model):
    assert len(view_model.done_items) == 1
    assert view_model.done_items[0].title == 'done-title'


def test_show_all_done_items_is_true_for_four_done_items(to_do_item, doing_item, done_item):
    test_view_model = ViewModel(
        [
            done_item,
            done_item,
            done_item,
            done_item
        ]
    )

    assert test_view_model.show_all_done_items


def test_show_all_done_items_is_true_for_four_done_items_and_other_items(to_do_item, doing_item, done_item):
    test_view_model = ViewModel(
        [
            done_item,
            done_item,
            done_item,
            done_item,
            to_do_item,
            doing_item,
        ]
    )

    assert test_view_model.show_all_done_items


def test_show_all_done_items_is_false_for_five_done_items(to_do_item, doing_item, done_item):
    test_view_model = ViewModel(
        [
            done_item,
            done_item,
            done_item,
            done_item,
            done_item
        ]
    )

    assert not test_view_model.show_all_done_items


def test_show_all_done_items_is_false_for_five_done_items_and_other_items(to_do_item, doing_item, done_item):
    test_view_model = ViewModel(
        [
            done_item,
            done_item,
            done_item,
            done_item,
            done_item,
            to_do_item,
            doing_item
        ]
    )

    assert not test_view_model.show_all_done_items
