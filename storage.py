
import os
from typing import Union
import argparse
import json


def create_file(db: str) -> None:
    """Создает пустой файл"""
    with open(db, 'w'):
        pass


def read_database(key: Union[str, None] = None, *, db: str = 'storage.data') -> Union[str, None]:
    """Читает файл.
    Если файла нет, создает его при помощи create_file().
    Если key == None, возвращает базу целиком.
    Если база пустая, возвращает None.
    Если key есть в базе, возвращает values в виде строки.
    Если key нет в базе, возвращает None"""
    if not os.path.isfile(db):
        create_file(db)
    with open(db, 'r') as database:
        data = database.read()
        if not key:
            return data
        else:
            if not data:
                return None
            else:
                data = json.loads(data)
                if key in data:
                    return ', '.join(data[key])
                else:
                    return None


def write_database(key: str, value: str, db: str = 'storage.data') -> None:
    """Записывает в файл.
    Если база пустая, добавляет в нее {key: [value]}.
    Если ключ есть в базе, добавляет value.
    Если ключа нет в базе, добавляет data[key] = [value]"""
    data = read_database()
    if not data:
        data = {key: [value]}
    else:
        data = json.loads(data)
        if key in data:
            data[key].append(value)
        else:
            data[key] = [value]
    with open(db, 'w') as database:
        json.dump(data, database)


def storage():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', help='The key by which the value is stored in the database')
    parser.add_argument('--value', help='The value that is stored in the database')
    att = parser.parse_args()
    if att.key and att.value:
        write_database(att.key, att.value)
    elif att.key and not att.value:
        print(read_database(att.key))
    else:
        print('Invalid input')


if __name__ == "__main__":
    storage()