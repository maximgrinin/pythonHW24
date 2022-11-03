import os
import re
from typing import Iterable
from flask import Flask, request, abort, Response

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

app = Flask(__name__)


def file_reader(file: str) -> Iterable[str]:
    with open(file) as f:
        counter = 0
        while True:
            try:
                line = next(f)
            except StopIteration:
                break
            yield line
            counter += 1


def filter_func(log_arg: Iterable[str], content: str) -> Iterable[str]:
    return filter(lambda log_item: content in log_item, log_arg)


def map_func(log_arg: Iterable[str], col: int) -> Iterable[str]:
    return map(lambda log_item: log_item.split(' ')[col], log_arg)


def unique_func(log_arg: Iterable[str]) -> Iterable[str]:  # -> set:
    return set(log_arg)


def sort_func(log_arg: Iterable[str], direction: str) -> Iterable[str]:
    return sorted(log_arg, reverse=True if direction == 'desc' else False)


def limit_func(log_arg: Iterable[str], quantity: int) -> Iterable[str]:
    return [x for i, x in enumerate(log_arg) if i < quantity]


def regex_func(log_arg: Iterable[str], regex: str) -> Iterable[str]:
    try:
        compiled_regex = re.compile(regex)
    except re.error as e:
        raise e
    return [log_item for log_item in log_arg if compiled_regex.search(log_item)]


@app.post("/perform_query")
def perform_query() -> Response:
    # нужно взять код из предыдущего ДЗ
    # добавить команду regex
    # добавить типизацию в проект, чтобы проходила утилиту mypy app.py

    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    if not all((request.form.get("cmd1", ""), request.form.get("value1", ""), request.form.get("file_name", ""))):
        abort(400)

    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    data_file_name: str = os.path.join(DATA_DIR, request.form.get("file_name", "apache_logs.txt"))
    if not os.path.exists(data_file_name):
        abort(400)

    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат
    log: Iterable[str] = file_reader(data_file_name)
    args: dict = dict(zip({v: '' for k, v in request.form.to_dict().items() if k[:3] == 'cmd'},
                          {v: '' for k, v in request.form.to_dict().items() if k[:3] == 'val'}))
    for k, v in args.items():
        match k:
            case 'filter':
                log = filter_func(log, v)
            case 'map':
                try:
                    log = map_func(log, int(v))
                except ValueError:
                    abort(400)
            case 'unique':
                log = unique_func(log)
            case 'sort':
                log = sort_func(log, v)
            case 'limit':
                try:
                    log = limit_func(log, int(v))
                except ValueError:
                    abort(400)
            case 'regex':
                try:
                    log = regex_func(log, v)
                except ValueError:
                    abort(400)

    return app.response_class("\n".join(list(log)), content_type="text/plain")


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
