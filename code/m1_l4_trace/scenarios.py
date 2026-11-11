"""Сценарии инцидента 4 для тестов и тренажера сбоев. Запуск отдельно: python scenarios.py task"""
import copy
import importlib
import json
import sys

from traces import CASES

TITLE = "Инцидент 4. Проверка трассы: полная ли выгрузка"
FUNCTION = "check_trace"


def run(func):
    results = []
    for name, trace, total, want in CASES:
        try:
            got = func(copy.deepcopy(trace), total)
        except Exception as error:
            got = f"исключение {type(error).__name__}: {error}"
        ok = got == want
        results.append({"name": name, "ok": ok, "message": "" if ok else
                        f"трасса {trace}, total={total}: ожидалось {want}, получено {got}"})
    return results


if __name__ == "__main__":
    module = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 else "task")
    print(json.dumps({"title": TITLE, "results": run(getattr(module, FUNCTION))}))
