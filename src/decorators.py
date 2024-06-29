from functools import wraps
from typing import Any, Callable


def reports(filename: str = "reports") -> Callable[[Any], Any]:
    """
    Декоратор, который записывает в файл результат, который возвращает функция, формирующая отчет.
    """

    def wrapper(function: Callable[[Any], Any]) -> Callable[[Any], Any]:
        @wraps(function)
        def inner(*args: Any, **kwargs: Any) -> Any:
            with open(f"{filename}.txt", "a", encoding="utf8") as file:
                try:
                    result = function(*args, **kwargs)
                except Exception as error:
                    file.write(
                        f"{function.__name__} error: {type(error).__name__}"
                        f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
                    )
                else:
                    file.write(
                        f"{function.__name__} ok \nresult: {result}\n---------------------------------\n"
                    )
                    return result

        return inner

    return wrapper
