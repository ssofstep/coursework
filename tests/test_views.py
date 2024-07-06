import json
from unittest.mock import patch, Mock

import pytest

from src.views import major


@pytest.fixture
def data() -> list:
    return [
        {
            "Дата операции": "05.03.2018 14:58:38",
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
            "Дата операции": "25.03.2018 15:00:41",
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
            "Дата операции": "25.03.2018 14:05:08",
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
            "Дата операции": "25.03.2018 20:27:51",
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
            "Дата операции": "25.03.2018 12:49:53",
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


@patch("src.views.read_json_file")
@patch("src.views.read_xls_file")
@patch("src.views.stocks")
@patch("src.views.currency")
def test_major(mock_currency: Mock, mock_stock: Mock, mock_exel: Mock, mock_json: Mock, data: list) -> None:
    mock_currency.return_value = [{"conversion_rates": {"RUB": 52}}]
    mock_stock.return_value = [{"stock": "AAPL", "price": "175.7300"}]
    mock_exel.return_value = data
    mock_json.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    assert major("2018-03-30 14:23:05") == json.dumps(
        {
            "greeting": "Добрый день",
            "cards": [
                {"last_digit:": "7197", "total_spent:": 1920.9, "cashback:": 19.209}
            ],
            "top_transaction": [
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
            ],
            "currency_rates": [{"conversion_rates": {"RUB": 52}}],
            "stock_prices": [{"stock": "AAPL", "price": "175.7300"}],
        },
        ensure_ascii=False,
    )
