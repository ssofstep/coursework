import json
import os
from typing import Any

from src.utils import read_xls_file, suitable_transctions


def simple_search(word: str) -> Any:
    """Функция, которая возвращает JSON-ответ со всеми транзакциями, содержащими запрос в описании или категории"""
    xls_file = read_xls_file(os.path.join("..", "data", "operations.xls"))
    suit = suitable_transctions(xls_file, word)
    return json.dumps(suit, ensure_ascii=False)
