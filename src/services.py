import json
import os
from typing import Any

from src.logger import setup_logger
from src.utils import read_xls_file, suitable_transactions

logger = setup_logger("services", "services.log")


def simple_search(word: str) -> Any:
    """Функция, которая возвращает JSON-ответ со всеми транзакциями, содержащими запрос в описании или категории"""
    logger.info("get the path to the xls file and convert it")
    xls_file = read_xls_file(os.path.join("..", "data", "operations.xls"))
    suit = suitable_transactions(xls_file, word)
    logger.info("found files converted to json")
    return json.dumps(suit, ensure_ascii=False)
