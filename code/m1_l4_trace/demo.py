"""Запуск: python demo.py

Печатает пять трасс и находки, которые должна выдать по ним проверка.
"""
from traces import CASES

if __name__ == "__main__":
    for name, trace, total, findings in CASES[:5]:
        print(name)
        for offset, limit, ids in trace:
            print(f"  offset={offset} limit={limit} -> {ids}")
        print(f"  API сообщил total={total}")
        print(f"  находки: {findings or 'нет'}")
        print()
