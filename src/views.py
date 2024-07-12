import json
import os.path
from datetime import datetime, timedelta

import pandas as pd

from src.logger import setup_logger
from src.utils import (
    currency,
    each_card,
    filter_by_date,
    greeting_message,
    read_json_file,
    stocks,
    top_transactions,
)

logger = setup_logger("views", "views.log")


def major(transactions: pd.DataFrame, date_time: str) -> str:
    """Функция, которая принимает на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
    и возвращающую JSON-ответ со следующими данными"""
    greeting = greeting_message(date_time)
    logger.info(f"Приветствие - {greeting}")
    date_time_dt = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    date_end = date_time_dt - timedelta(days=int(date_time_dt.strftime("%d")) - 1)
    list_transactions = transactions.to_dict(orient="records")
    logger.info("Получили список операций")
    list_transactions = filter_by_date(date_time_dt, date_end, list_transactions)
    cards = each_card(list_transactions)
    logger.info("Рассчитали общую сумму трат и кешбэк каждой карты")
    top_transaction = top_transactions(list_transactions)
    logger.info("Вычислили топ 5 транзакций по сумме платежа")
    json_file = read_json_file(os.path.join("..", "user_settings.json"))
    logger.info("Загружаем json-файл с валютами и акциями")
    currency_rates = currency(json_file["user_currencies"])
    logger.info("Получаем текущие валюты")
    stock_prices = stocks(json_file["user_stocks"])
    logger.info("Получаем стоимость акций")
    result = {
        "greeting": greeting,
        "cards": cards,
        "top_transaction": top_transaction,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
    return json.dumps(result, indent=2, ensure_ascii=False)
