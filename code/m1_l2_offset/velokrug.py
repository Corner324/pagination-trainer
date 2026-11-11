"""Учебный API "ВелоКруга" в памяти: поездки отдаются страницами по offset/limit.

Сеть не нужна. Список поездок можно менять между запросами - так воспроизводится
сдвиг страниц. Новые поездки идут первыми (сортировка по убыванию id).
"""


class RidesApi:
    def __init__(self, ride_ids):
        self._ids = sorted(ride_ids, reverse=True)
        self.calls = []  # трасса: (offset, limit, что вернули)

    def get_page(self, offset, limit):
        page = self._ids[offset:offset + limit]
        self.calls.append((offset, limit, list(page)))
        return page

    def add_ride(self, ride_id):
        self._ids = sorted(self._ids + [ride_id], reverse=True)

    def remove_ride(self, ride_id):
        self._ids.remove(ride_id)
