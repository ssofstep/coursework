from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from src.decorators import reports
from src.logger import setup_logger

logger = setup_logger("reports", "reports.log")


@reports()
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    """Функция, которая возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
    logger.info("Получаем дату и время или берём текущие")
    if date is None:
        date_time = datetime.now()
    else:
        date_time = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    transactions = transactions[transactions["Сумма операции"] < 0]
    transactions = transactions[transactions["Категория"] == category]
    end_date = date_time - timedelta(days=90)
    logger.info("Фильтруем по категории и тратам")
    transactions = transactions[
        pd.to_datetime(transactions["Дата операции"], dayfirst=True) <= date_time
    ]
    logger.info("Сравнивем с верхней границей даты")
    transactions = transactions[
        pd.to_datetime(transactions["Дата операции"], dayfirst=True) > end_date
    ]
    logger.info("Сравнивем с нижней границей даты")
    return pd.DataFrame(transactions)
