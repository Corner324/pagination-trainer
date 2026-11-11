"""Тренажер сбоев "ВелоКруга". Запуск из папки code:  python trainer.py

Прогоняет ваши решения (файлы task.py в папках уроков) через все сценарии сбоев
и печатает отчет. Подробности по проваленному сценарию:  python trainer.py -v
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def run_lesson(folder, module):
    done = subprocess.run([sys.executable, "-B", "scenarios.py", module], cwd=os.path.join(HERE, folder),
                          capture_output=True, text=True, encoding="utf-8")
    try:
        return json.loads(done.stdout.strip().splitlines()[-1])
    except (IndexError, ValueError):
        last = (done.stderr.strip().splitlines() or ["нет вывода"])[-1]
        return {"title": folder, "results": [{"name": "файл решения запускается", "ok": False, "message": last}]}


def main():
    verbose = "-v" in sys.argv
    module = "solution" if "--solution" in sys.argv else "task"
    lessons = sorted(d for d in os.listdir(HERE)
                     if os.path.isfile(os.path.join(HERE, d, "scenarios.py")))
    passed = total = 0
    print('Тренажер сбоев "ВелоКруга"')
    for folder in lessons:
        report = run_lesson(folder, module)
        ok = sum(r["ok"] for r in report["results"])
        passed, total = passed + ok, total + len(report["results"])
        print(f"\n{report['title']}  -  {ok} из {len(report['results'])}")
        for r in report["results"]:
            print(f"  [{'прошел' if r['ok'] else 'ПРОВАЛ'}] {r['name']}")
            if verbose and not r["ok"]:
                print(f"           {r['message']}")
    print(f"\nИтог: пройдено {passed} из {total} сценариев.")
    if passed < total and not verbose:
        print("Что именно пошло не так:  python trainer.py -v")
    print("Отчет говорит о сценариях тренажера. Он не доказывает, что загрузчик переживет любой сбой любого API.")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
