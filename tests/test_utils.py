import json
import os
from datetime import datetime
from typing import Any
from unittest.mock import Mock, patch

from dotenv import load_dotenv
from pandas import DataFrame

from src.utils import (
    currency,
    each_card,
    filter_by_date,
    greeting_message,
    read_json_file,
    read_xls_file,
    stocks,
    suitable_transactions,
    top_transactions,
)


@patch("pandas.read_excel")
def test_read_xlsx_file(mock_open: Mock) -> None:
    mock_open.return_value = DataFrame(
        {
            "id": [650703.0],
            "state": ["EXECUTED"],
            "date": ["2023-09-05T11:30:32Z"],
            "amount": [16210.0],
            "currency_name": ["Sol"],
            "currency_code": ["PEN"],
            "from": ["Счет 58803664561298323391"],
            "to": ["Счет 39745660563456619397"],
            "description": ["Перевод организации"],
        }
    )
    assert read_xls_file(os.path.join("..", "data", "operations.xls")) == [
        {
            "id": 650703.0,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210.0,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        }
    ]


@patch("builtins.open")
def test_read_json_file(mock_open: Mock) -> None:
    mock_file = mock_open.return_value.__enter__.return_value
    mock_file.read.return_value = json.dumps(
        [
            {
                "user_currencies": ["USD", "EUR"],
                "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
            }
        ]
    )
    assert read_json_file(os.path.join("..", "user_settings.json")) == [
        {
            "user_currencies": ["USD", "EUR"],
            "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
        }
    ]


def test_suitable_transactions() -> None:
    data = [
        {
            "Дата операции": "01.01.2018 20:27:51",
            "Дата платежа": "04.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -316.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -316.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "",
            "Категория": "Красота",
            "MCC": 5977.0,
            "Описание": "OOO Balid",
            "Бонусы (включая кэшбэк)": 6,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 316.0,
        },
        {
            "Дата операции": "01.01.2018 12:49:53",
            "Дата платежа": "01.01.2018",
            "Номер карты": "",
            "Статус": "OK",
            "Сумма операции": -3000.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -3000.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "",
            "Категория": "Переводы",
            "MCC": "",
            "Описание": "Линзомат ТЦ Юность",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 3000.0,
        },
    ]
    assert suitable_transactions(data, "Переводы") == [
        {
            "Дата операции": "01.01.2018 12:49:53",
            "Дата платежа": "01.01.2018",
            "Номер карты": "",
            "Статус": "OK",
            "Сумма операции": -3000.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -3000.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "",
            "Категория": "Переводы",
            "MCC": "",
            "Описание": "Линзомат ТЦ Юность",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 3000.0,
        }
    ]


def test_greeting_message() -> None:
    assert greeting_message("2024-07-02 11:32:45") == "Доброе утро"


def test_each_card() -> None:
    data = [
        {
            "Дата операции": "01.01.2018 20:27:51",
            "Дата платежа": "04.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -316.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -316.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Красота",
            "MCC": 5977.0,
            "Описание": "OOO Balid",
            "Бонусы (включая кэшбэк)": 6,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 316.0,
        },
        {
            "Дата операции": "01.01.2018 12:49:53",
            "Дата платежа": "01.01.2018",
            "Номер карты": None,
            "Статус": "OK",
            "Сумма операции": -3000.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -3000.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Переводы",
            "MCC": None,
            "Описание": "Линзомат ТЦ Юность",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 3000.0,
        },
    ]
    assert each_card(data) == [{"last_digit:": "7197", "total_spent:": 316.0, "cashback:": 3.16}]


def test_top_transactions() -> None:
    data = [
        {
            "Дата операции": "05.01.2018 14:58:38",
            "Дата платежа": "07.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -120.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -120.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Цветы",
            "MCC": 5992.0,
            "Описание": "Magazin  Prestizh",
            "Бонусы (включая кэшбэк)": 2,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 120.0,
        },
        {
            "Дата операции": "04.01.2018 15:00:41",
            "Дата платежа": "05.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -1025.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -1025.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Топливо",
            "MCC": 5541.0,
            "Описание": "Pskov AZS 12 K2",
            "Бонусы (включая кэшбэк)": 20,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 1025.0,
        },
        {
            "Дата операции": "04.01.2018 14:05:08",
            "Дата платежа": "06.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": 1065.9,
            "Валюта операции": "RUB",
            "Сумма платежа": -1065.9,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Супермаркеты",
            "MCC": 5411.0,
            "Описание": "Пятёрочка",
            "Бонусы (включая кэшбэк)": 21,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 1065.9,
        },
        {
            "Дата операции": "01.01.2018 20:27:51",
            "Дата платежа": "04.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -316.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -316.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Красота",
            "MCC": 5977.0,
            "Описание": "OOO Balid",
            "Бонусы (включая кэшбэк)": 6,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 316.0,
        },
        {
            "Дата операции": "01.01.2018 12:49:53",
            "Дата платежа": "01.01.2018",
            "Номер карты": None,
            "Статус": "OK",
            "Сумма операции": -3000.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -3000.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Переводы",
            "MCC": None,
            "Описание": "Линзомат ТЦ Юность",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 3000.0,
        },
        {
            "Дата операции": "27.03.2018 18:11:05",
            "Дата платежа": "29.03.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -159.9,
            "Валюта операции": "RUB",
            "Сумма платежа": -159.9,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Супермаркеты",
            "MCC": 5411.0,
            "Описание": "Перекрёсток",
            "Бонусы (включая кэшбэк)": 3,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 159.9,
        },
        {
            "Дата операции": "27.03.2018 17:50:54",
            "Дата платежа": "29.03.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -300.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -300.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Ж/д билеты",
            "MCC": 4111.0,
            "Описание": "Московский метрополитен",
            "Бонусы (включая кэшбэк)": 6,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 300.0,
        },
    ]
    assert top_transactions(data) == [
        {
            "date": "01.01.2018",
            "amount": 3000.0,
            "category": "Переводы",
            "description": "Линзомат ТЦ Юность",
        },
        {
            "date": "05.01.2018",
            "amount": 1025.0,
            "category": "Топливо",
            "description": "Pskov AZS 12 K2",
        },
        {
            "date": "04.01.2018",
            "amount": 316.0,
            "category": "Красота",
            "description": "OOO Balid",
        },
        {
            "date": "29.03.2018",
            "amount": 300.0,
            "category": "Ж/д билеты",
            "description": "Московский метрополитен",
        },
        {
            "date": "29.03.2018",
            "amount": 159.9,
            "category": "Супермаркеты",
            "description": "Перекрёсток",
        },
    ]


load_dotenv()
api_token_currency = os.getenv("API_KEY_CURRENCY")
headers_ = {"apikey": api_token_currency}
payload_: dict[Any, Any] = {}


@patch("requests.get")
def test_currency(mock_get: Mock) -> None:
    mock_get.return_value.json.return_value = {"conversion_rates": {"RUB": 52}}
    assert currency(["USD"]) == [{"currency": "USD", "rate": 52}]


load_dotenv()
api_token_stocks = os.getenv("API_KEY_STOCKS")
headers = {"apikey": api_token_stocks}
payload: dict[Any, Any] = {}


@patch("requests.get")
def test_stocks(mock_get: Mock) -> None:
    mock_get.return_value.json.return_value = {
        "Time Series (1min)": {
            "2024-07-03 17:00:00": {
                "1. open": "175.7300",
                "2. high": "175.7300",
                "3. low": "175.7300",
                "4. close": "175.7300",
                "5. volume": "435052",
            }
        }
    }
    assert stocks(["AAPL"]) == [{"stock": "AAPL", "price": "175.7300"}]


def test_filter_by_date() -> None:
    data = [
        {"Дата операции": "31.12.2021 16:44:00"},
        {"Дата операции": "30.12.2021 17:50:30"},
        {"Дата операции": "01.12.2021 17:50:30"},
        {"Дата операции": "01.11.2020 17:50:30"},
    ]
    date = datetime.strptime("31.12.2021 16:44:00", "%d.%m.%Y %H:%M:%S")
    date_end = datetime.strptime("01.12.2021 16:44:00", "%d.%m.%Y %H:%M:%S")
    assert filter_by_date(date, date_end, data) == [
        {"Дата операции": "31.12.2021 16:44:00"},
        {"Дата операции": "30.12.2021 17:50:30"},
        {"Дата операции": "01.12.2021 17:50:30"},
    ]
