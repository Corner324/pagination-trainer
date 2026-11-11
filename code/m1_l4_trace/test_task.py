"""Проверка вашего решения из task.py. Запуск из этой папки: python -m unittest"""
import importlib
import os
import unittest

from scenarios import FUNCTION, run


def check(func):
    """Возвращает список сообщений об ошибках; пустой список - решение верное."""
    return [f"Сценарий '{r['name']}': {r['message']}" for r in run(func) if not r["ok"]]


class TestTask(unittest.TestCase):
    def test_task(self):
        module = importlib.import_module("task")
        self.assertEqual(check(getattr(module, FUNCTION)), [])


if __name__ == "__main__":
    unittest.main()
