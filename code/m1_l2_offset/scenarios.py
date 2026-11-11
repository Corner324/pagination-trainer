"""Сценарии инцидента 2 для тестов и тренажера сбоев. Запуск отдельно: python scenarios.py task"""
import importlib
import json
import sys

TITLE = "Инцидент 2. Сдвиг страниц: дубли и потери по трассе"
FUNCTION = "diff_trace"

CASES = [
    # (название, expected, pages, lost, duplicated)
    ("данные не менялись",
     [100, 101, 102, 103, 104, 105], [[105, 104, 103], [102, 101, 100]], [], []),
    ("появилась новая поездка 106: 103 пришла дважды",
     [100, 101, 102, 103, 104, 105], [[105, 104, 103], [103, 102, 101], [100]], [], [103]),
    ("удалили 104: 102 не пришла ни разу",
     [100, 101, 102, 103, 104, 105], [[105, 104, 103], [101, 100]], [102], []),
    ("новая поездка в выдаче не считается потерянной",
     [100, 101, 102], [[103, 102, 101], [101, 100]], [], [101]),
    ("запись пришла трижды - в ответе она один раз",
     [1, 2, 3], [[3, 2], [2, 1], [2]], [], [2]),
    ("ответ отсортирован по возрастанию",
     [5, 4, 3, 2, 1], [[5, 5], [3, 3]], [1, 2, 4], [3, 5]),
    ("пустая трасса: потеряно все",
     [1, 2], [], [1, 2], []),
]


def run(func):
    results = []
    for name, expected, pages, lost, duplicated in CASES:
        try:
            got = func(list(expected), [list(p) for p in pages])
        except Exception as error:
            got = f"исключение {type(error).__name__}: {error}"
        ok = got == (lost, duplicated)
        results.append({"name": name, "ok": ok, "message": "" if ok else
                        f"страницы {pages}: ожидалось {(lost, duplicated)}, получено {got}"})
    return results


if __name__ == "__main__":
    module = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 else "task")
    print(json.dumps({"title": TITLE, "results": run(getattr(module, FUNCTION))}))
