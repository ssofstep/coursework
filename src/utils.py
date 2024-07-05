import os
from datetime import datetime, time
from typing import Any
import json
import pandas as pd
import requests
from dotenv import load_dotenv

from src.logger import setup_logger

logger = setup_logger("utils", "utils.log")


def read_xls_file(path: str) -> list:
    """Функция, которая считывает финансовые операции с XLS-файла"""
    logger.info("get the path to the xls file")
    xls_file = pd.read_excel(path)
    xls_dict = xls_file.to_dict(orient="records")
    logger.info("the converted file")
    return xls_dict


def read_json_file(path: str) -> dict[Any, Any]:
    with open(path, "r", encoding="utf8") as file:
        return json.load(file)


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
    """Функция, которая формирует JSON-ответ с картами, где есть общая сумма трат, кешбэк и последние 4 цифры карты"""
    dict_summ: dict = {}
    dict_cashback: dict = {}
    logger.info("Распределяем по номерам  карт общий кешбэк и сумму операций")
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
    logger.info("Соединяем словарики и формируем JSON-ответ")
    for k, v in dict_summ.items():
        list_card.append(
            {
                "last_digit:": k[-4:],
                "total_spent:": v,
                "cashback:": dict_cashback.get(k, 0),
            }
        )
    return list_card


def top_transactions(transactions: list[dict]) -> list[dict]:
    """Функция, которая возвращает топ-5 транзакций по сумме платежа"""
    list_transactions = []
    logger.info(
        "Фильтруем список транзакций: добавляем только траты и преобразовываем их в +"
    )
    for i in transactions:
        if i["Сумма операции"] < 0:
            i["Сумма операции"] = i["Сумма операции"] * -1
            list_transactions.append(i)
    max_transactions = []
    logger.info(
        "Добавляем в список max_transactions топ-5 транзакций по сумме операции"
    )
    for item in range(5):
        max_transaction = max(list_transactions, key=lambda x: x["Сумма операции"])
        max_transactions.append(
            {
                "date": max_transaction["Дата платежа"],
                "amount": max_transaction["Сумма операции"],
                "category": max_transaction["Категория"],
                "description": max_transaction["Описание"],
            }
        )
        list_transactions.remove(max_transaction)

    return max_transactions


load_dotenv()
api_token_currency = os.getenv("API_KEY_CURRENCY")


def currency(currency_list: list) -> list:
    """Функция, которая возвращает курс валют"""
    headers = {"apikey": api_token_currency}
    payload: dict[Any, Any] = {}
    list_rates = []
    for item in currency_list:
        url_usd = (
            f"https://v6.exchangerate-api.com/v6/{api_token_currency}/latest/{item}"
        )
        response = requests.get(url_usd, headers=headers, data=payload)
        currency_json_usd = response.json()
        usd_url_rates = currency_json_usd["conversion_rates"]["RUB"]
        logger.info(f"Курс валюты в рублях {usd_url_rates}")
        list_rates.append({"currency": item, "rate": usd_url_rates})

    return list_rates


load_dotenv()
api_token_stocks = os.getenv("API_KEY_STOCKS")


def stocks(stockes_list: list) -> list:
    headers = {"apikey": api_token_stocks}
    payload: dict[Any, Any] = {}
    list_stocks = []
    for item in stockes_list:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={item}&interval=1min&apikey={api_token_stocks}"
        response = requests.get(url, headers=headers, data=payload)
        stocks_json = response.json()
        url_stocks = stocks_json["Time Series (1min)"]
        stocks_sorted = sorted(url_stocks.keys())[0]
        stocks_prices = url_stocks[stocks_sorted]["4. close"]
        logger.info(f"Стоимость акций {stocks_prices}")
        list_stocks.append({"stock": item, "price": stocks_prices})
    return list_stocks
