"""Запуск: python demo.py

Наивный загрузчик на двух API: один за концом списка отдает пустую страницу,
другой - снова последнюю.
"""
from velokrug import RidesApi, TooManyCalls

LIMIT = 3
RIDES = [100, 101, 102, 103, 104, 105, 106]


def fetch_all(api):
    """Наивный загрузчик: идем по offset, пока страница не пустая."""
    rows, offset = [], 0
    while True:
        page = api.get_page(offset, LIMIT)
        if not page:
            return rows
        rows += page
        offset += LIMIT


def show(title, api, rows):
    print(title)
    for offset, limit, page in api.calls[:6]:
        print(f"  offset={offset} limit={limit} -> {page}")
    if len(api.calls) > 6:
        print(f"  ... всего запросов: {len(api.calls)}")
    print(f"  результат: {rows}")
    print()


if __name__ == "__main__":
    api = RidesApi(RIDES)
    show("1. За концом списка API отдает пустую страницу", api, fetch_all(api))

    api = RidesApi(RIDES, end="repeat_last")
    try:
        rows = fetch_all(api)
    except TooManyCalls as error:
        rows = f"загрузчик остановлен предохранителем учебного API: {error}"
    show("2. За концом списка API снова отдает последнюю страницу", api, rows)
