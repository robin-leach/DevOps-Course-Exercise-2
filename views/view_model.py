from entity.status import Status

from helpers.index import filter_items_by_list, filter_items_modified_today, filter_items_last_modified_before_today


class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def all_items(self):
        return self._items

    @property
    def to_do_items(self):
        return filter_items_by_list(self._items, Status.ToDo.value)

    @property
    def doing_items(self):
        return filter_items_by_list(self._items, Status.Doing.value)

    @property
    def done_items(self):
        return filter_items_by_list(self._items, Status.Done.value)

    @property
    def show_all_done_items(self):
        return len(self.done_items) < 5

    @property
    def recent_done_items(self):
        return filter_items_modified_today(self.done_items)

    @property
    def older_items(self):
        return filter_items_last_modified_before_today(self.done_items)

    @property
    def display_older_items(self):
        return len(self.older_items) > 0
