"""Запуск: python demo.py

Те же два события, что в инциденте 2, но обход идет по закладке, а не по offset.
"""
from velokrug import RidesApi

LIMIT = 3
START = [100, 101, 102, 103, 104, 105]


def fetch_all(api):
    rows, before = [], None
    while True:
        page = api.get_page(before, LIMIT)
        if not page:
            return rows
        rows += page
        before = page[-1]  # закладка: последняя поездка, которую мы уже получили


def show(title, api, rows):
    print(title)
    for before, limit, page in api.calls:
        print(f"  before={before} limit={limit} -> {page}")
    print(f"  загружено строк: {len(rows)}, уникальных поездок: {len(set(rows))}")
    print(f"  дубли: {sorted({r for r in rows if rows.count(r) > 1})}")
    print(f"  потеряны: {sorted(set(START) - set(rows))}")
    print()


if __name__ == "__main__":
    api = RidesApi(START)
    show("1. Данные не меняются", api, fetch_all(api))

    api = RidesApi(START, events={1: lambda a: a.add_ride(106)})
    show("2. После первой страницы появилась поездка 106", api, fetch_all(api))

    api = RidesApi(START, events={1: lambda a: a.remove_ride(104)})
    show("3. После первой страницы поездку 104 удалили", api, fetch_all(api))
