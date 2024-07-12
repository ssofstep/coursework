import json
from typing import Any

from src.logger import setup_logger
from src.utils import suitable_transactions

logger = setup_logger("services", "services.log")


def simple_search(transactions: list[dict], word: str) -> Any:
    """Функция, которая возвращает JSON-ответ со всеми транзакциями, содержащими запрос в описании или категории"""
    logger.info("get the path to the xls file and convert it")
    suit = suitable_transactions(transactions, word)
    logger.info("found files converted to json")
    return json.dumps(suit, ensure_ascii=False)
