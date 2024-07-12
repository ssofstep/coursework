import os.path

import pandas as pd

from src.reports import spending_by_category
from src.services import simple_search
from src.views import major
from src.utils import read_xls_file


def main() -> None:
    """Сброка проекта и всех функций в одну"""
    user_date = input("Введите текущую дату и время в формате YYYY-MM-DD HH:MM:SS")
    transactions_path = os.path.join("..", "data", "operations.xls")
    print(major(pd.read_excel(transactions_path), user_date))
    print("-------------------------------------")
    word = input("Введите слово для поиска опираций")
    print(simple_search(read_xls_file(transactions_path), word))
    print("-------------------------------------")
    category = input("Введите категорию, по которой будем считать траты")
    date = input("Введите дату, от которой надо будет считать траты в формате YYYY-MM-DD HH:MM:SS")
    print(spending_by_category(pd.read_excel(transactions_path), category, date))
    print("-------------------------------------")


if __name__ == "__main__":
    main()
