from pandas import DataFrame

from src.reports import spending_by_category


def test_spending_by_category() -> None:
    data = DataFrame(
        [
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
    )
    assert spending_by_category(data, "Переводы", "01.01.2018 20:27:51").to_dict(
        "records"
    ) == [
        {
            "MCC": "",
            "Бонусы (включая кэшбэк)": 0,
            "Валюта операции": "RUB",
            "Валюта платежа": "RUB",
            "Дата операции": "01.01.2018 12:49:53",
            "Дата платежа": "01.01.2018",
            "Категория": "Переводы",
            "Кэшбэк": "",
            "Номер карты": "",
            "Округление на инвесткопилку": 0,
            "Описание": "Линзомат ТЦ Юность",
            "Статус": "OK",
            "Сумма операции": -3000.0,
            "Сумма операции с округлением": 3000.0,
            "Сумма платежа": -3000.0,
        }
    ]
