from typing import Any

import pandas as pd

from src.logger import setup_logger

logger = setup_logger("utils", "utils.log")


def read_xls_file(path: str) -> list:
    """Функция, которая считывает финансовые операции с XLSX-файла"""
    logger.info("get the path to the xls file")
    xls_file = pd.read_excel(path)
    xls_dict = xls_file.to_dict(orient="records")
    logger.info("the converted file")
    return xls_dict


def suitable_transactions(xls_file: list[dict], search_line: str) -> Any:
    """Функция, которая возвращает список со всеми транзакциями, содержащими запрос в описании или категории"""
    logger.info(f"start searching for suitable dictionaries by word {search_line}")
    new_list = []
    for transaction in xls_file:
        if (
            search_line == transaction["Категория"]
            or search_line == transaction["Описание"]
        ):
            new_list.append(transaction)
    logger.info(f"found dictionaries by word {search_line}")
    return new_list
