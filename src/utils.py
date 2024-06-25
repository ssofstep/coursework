from typing import Any

import pandas as pd


def read_xls_file(path: str) -> list:
    """Функция, которая считывает финансовые операции с XLSX-файла"""
    xls_file = pd.read_excel(path)
    xls_dict = xls_file.to_dict(orient="records")
    return xls_dict


def suitable_transctions(xls_file: list[dict], search_line: str) -> Any:
    """Функция, которая возвращает список со всеми транзакциями, содержащими запрос в описании или категории"""
    new_list = []
    for transaction in xls_file:
        if (
            search_line == transaction["Категория"]
            or search_line == transaction["Описание"]
        ):
            new_list.append(transaction)
    return new_list
