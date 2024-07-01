from datetime import datetime, time
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


def greeting_message(date: str):
    """Функция, которая возвращает приветствие в зависимости от времени"""
    logger.info("Подбирает приветствие")
    date_time = datetime.strptime(date, "%d.%m.%Y %H:%M:%S").time()
    greeting_time = {
        "Доброй ночи": time(6, 0, 0),
        "Доброе утро": time(12, 0, 0),
        "Добрый день": time(17, 0, 0),
        "Добрый вечер": time(23, 0, 0),
    }

    for k, v in greeting_time.items():
        if date_time <= v:
            logger.info(f"Приветствие {k}")
            return k


def each_card(transactions: list[dict]) -> list[dict]:
    dict_summ: dict = {}
    dict_cashback: dict = {}
    for i in transactions:
        if isinstance(i["Номер карты"], str) and i["Сумма операции"] < 0:
            dict_summ[i["Номер карты"]] = (
                dict_summ.get(i["Номер карты"], 0) + i["Сумма операции"] * -1
            )
            if i["Сумма операции"] * -1 > 100:
                dict_cashback[i["Номер карты"]] = (
                    dict_cashback.get(i["Номер карты"], 0)
                    + (i["Сумма операции"] * -1) / 100
                )
    list_card = []
    for k, v in dict_summ.items():
        list_card.append(
            {
                "last_digit:": k[-4:],
                "total_spent:": v,
                "cashback:": dict_cashback.get(k, 0),
            }
        )
    return list_card
