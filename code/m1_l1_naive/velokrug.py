"""Учебный API "ВелоКруга" в памяти: поездки страницами по offset/limit, новые первыми.

end="empty"       - за концом списка API отдает пустую страницу;
end="repeat_last" - за концом списка API снова отдает последнюю страницу (так делают некоторые API).
"""


class TooManyCalls(Exception):
    """Предохранитель учебного API: загрузчик сделал подозрительно много запросов."""


class RidesApi:
    def __init__(self, ride_ids, end="empty", call_cap=50):
        self._ids = sorted(ride_ids, reverse=True)
        self._end = end
        self._call_cap = call_cap
        self.calls = []  # трасса: (offset, limit, что вернули)

    def get_page(self, offset, limit):
        if len(self.calls) >= self._call_cap:
            raise TooManyCalls(f"больше {self._call_cap} запросов - похоже на бесконечный цикл")
        page = self._ids[offset:offset + limit]
        if not page and self._end == "repeat_last":
            page = self._ids[(len(self._ids) - 1) // limit * limit:]
        self.calls.append((offset, limit, list(page)))
        return page
