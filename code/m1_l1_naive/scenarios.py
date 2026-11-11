"""Сценарии инцидента 1 для тестов и тренажера сбоев.

run(func) возвращает список словарей: name - сценарий, ok - пройден ли, message - что не так.
Запуск отдельно: python scenarios.py task
"""
import importlib
import json
import sys

from velokrug import RidesApi

TITLE = "Инцидент 1. Обход по страницам: когда остановиться"
FUNCTION = "fetch_all"


def run(func):
    results = []

    def add(name, message):
        results.append({"name": name, "ok": message is None, "message": message or ""})

    def case(name, ride_ids, limit, want):
        api = RidesApi(ride_ids)
        try:
            got = func(api.get_page, limit)
        except Exception as error:
            got = f"исключение {type(error).__name__}: {error}"
        requests = [(o, p) for o, _, p in api.calls]
        if got != want:
            add(name, f"поездки {sorted(ride_ids, reverse=True)}, limit={limit}: "
                      f"ожидалось {want}, получено {got}. Запросы: {requests}")
        elif not api.calls or api.calls[-1][2] != []:
            add(name, f"данные верные, но загрузчик не дождался пустой страницы - "
                      f"конец списка не подтвержден. Запросы: {requests}")
        else:
            add(name, None)

    case("поездок нет", [], 3, [])
    case("одна неполная страница", [1, 2], 3, [2, 1])
    case("ровно две полные страницы", [1, 2, 3, 4, 5, 6], 3, [6, 5, 4, 3, 2, 1])
    case("последняя страница неполная", [1, 2, 3, 4, 5, 6, 7], 3, [7, 6, 5, 4, 3, 2, 1])
    case("limit=1", [10, 20], 1, [20, 10])

    name = "API за концом списка повторяет последнюю страницу"
    api = RidesApi([1, 2, 3, 4, 5, 6], end="repeat_last")
    try:
        got = func(api.get_page, 3, max_pages=5)
        add(name, f"ожидалось RuntimeError, а функция вернула {got}")
    except RuntimeError:
        if len(api.calls) != 5:
            add(name, f"при max_pages=5 должно быть ровно 5 запросов, сделано {len(api.calls)}")
        else:
            add(name, None)
    except Exception as error:
        add(name, f"ожидалось RuntimeError, получено {type(error).__name__}: {error}")
    return results


if __name__ == "__main__":
    module = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 else "task")
    print(json.dumps({"title": TITLE, "results": run(getattr(module, FUNCTION))}))
