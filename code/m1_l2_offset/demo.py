"""Запуск: python demo.py

Показывает, как наивный загрузчик получает дубль и теряет запись,
хотя ни один запрос не упал.
"""
from velokrug import RidesApi

LIMIT = 3
START = [100, 101, 102, 103, 104, 105]


def fetch_all(api, between_pages=None):
    """Наивный загрузчик: идем по offset, пока страницы не кончатся."""
    rows, offset = [], 0
    while True:
        page = api.get_page(offset, LIMIT)
        if not page:
            return rows
        rows += page
        offset += LIMIT
        if between_pages:
            between_pages(api)
            between_pages = None  # событие случается один раз, после первой страницы


def show(title, api, rows):
    print(title)
    for offset, limit, page in api.calls:
        print(f"  offset={offset} limit={limit} -> {page}")
    print(f"  загружено строк: {len(rows)}, уникальных поездок: {len(set(rows))}")
    print(f"  дубли: {sorted({r for r in rows if rows.count(r) > 1})}")
    print(f"  потеряны: {sorted(set(START) - set(rows))}")
    print()


if __name__ == "__main__":
    api = RidesApi(START)
    show("1. Данные не меняются", api, fetch_all(api))

    api = RidesApi(START)
    show("2. После первой страницы появилась поездка 106", api,
         fetch_all(api, lambda a: a.add_ride(106)))

    api = RidesApi(START)
    show("3. После первой страницы поездку 104 удалили", api,
         fetch_all(api, lambda a: a.remove_ride(104)))
