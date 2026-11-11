"""Учебный API "ВелоКруга" в памяти: поездки по закладке (курсору), новые первыми.

get_page(before, limit) отдает поездки с id меньше before. before=None - с самого начала.
events - что происходит с данными после запроса с данным номером: {1: функция(api)}.
"""


class TooManyCalls(Exception):
    """Предохранитель учебного API: загрузчик сделал подозрительно много запросов."""


class RidesApi:
    def __init__(self, ride_ids, events=None, ignores_cursor=False, call_cap=50):
        self._ids = sorted(ride_ids, reverse=True)
        self._events = events or {}
        self._ignores_cursor = ignores_cursor
        self._call_cap = call_cap
        self.calls = []  # трасса: (before, limit, что вернули)

    def get_page(self, before, limit):
        if len(self.calls) >= self._call_cap:
            raise TooManyCalls(f"больше {self._call_cap} запросов - похоже на бесконечный цикл")
        if before is None or self._ignores_cursor:
            candidates = self._ids
        else:
            candidates = [ride_id for ride_id in self._ids if ride_id < before]
        page = candidates[:limit]
        self.calls.append((before, limit, list(page)))
        event = self._events.get(len(self.calls))
        if event:
            event(self)
        return page

    def add_ride(self, ride_id):
        self._ids = sorted(self._ids + [ride_id], reverse=True)

    def remove_ride(self, ride_id):
        self._ids.remove(ride_id)
