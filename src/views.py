from typing import Any

from src.utils import greeting_message, each_card, top_transactions, currency, stocks, read_xls_file, read_json_file


def major(date_time: str) -> dict[Any, Any]:
    greeting = greeting_message(date_time)
    list_transactions = read_xls_file("..\\data\\operations.xls")
    cards = each_card(list_transactions)
    top_transaction = top_transactions(list_transactions)
    json_file = read_json_file("..\\user_settings.json")
    currency_rates = currency(json_file["user_currencies"])
    stock_prices = stocks(json_file["user_stocks"])
    return {"greeting": greeting, "cards": cards, "top_transaction": top_transaction, "currency_rates": currency_rates,
            "stock_prices": stock_prices}
