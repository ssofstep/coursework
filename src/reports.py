from datetime import datetime, timedelta
from typing import Optional
from src.utils import suitable_transactions, read_xls_file
import pandas as pd

from src.logger import setup_logger

logger = setup_logger("masks", "reports.log")


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция, которая возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
    if date is None:
        date_time = datetime.now()
    else:
        date_time = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    starting_date = date_time - timedelta(days=90)
    choiced_transactions = suitable_transactions(transactions, category)
    spending_transactions = []
    for i in choiced_transactions:
        if datetime.strptime(i["Дата операции"], "%d.%m.%Y %H:%M:%S") >= starting_date:
            spending_transactions.append(i)
    return spending_transactions


rd = read_xls_file("C:\\Users\\Sonya\\lecture\\coursework\\data\\operations.xls")
print(spending_by_category(rd, "Переводы", "31.12.2021 16:44:00"))
