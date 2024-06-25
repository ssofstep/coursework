import json
import os

from src.utils import read_xls_file, suitable_transctions


def simple_search():
    """Функция, которая возвращает JSON-ответ со всеми транзакциями, содержащими запрос в описании или категории"""
    xls_file = read_xls_file(os.path.join("..", "data", "operations.xls"))
    suit = suitable_transctions(xls_file, "Переводы")
    return json.dumps(suit, ensure_ascii=False)
