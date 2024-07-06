from typing import Callable

import pytest

from src.decorators import reports


@reports()
def summ_1(a: int, b: int) -> int:
    return a + b


@reports("text_file")
def summ_2(a: int, b: int) -> int:
    return a + b


@pytest.mark.parametrize(
    "func, a, b, string, name, correct",
    (
        [
            summ_1,
            3,
            2,
            3,
            "reports.txt",
            ["summ_1 ok", "result: 5", "---------------------------------"],
        ],
        [
            summ_1,
            3,
            "2",
            2,
            "reports.txt",
            ["summ_1 error: TypeError", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"],
        ],
        [
            summ_2,
            3,
            2,
            3,
            "text_file.txt",
            ["summ_2 ok", "result: 5", "---------------------------------"],
        ],
        [
            summ_2,
            3,
            "2",
            2,
            "text_file.txt",
            ["summ_2 error: TypeError", "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"],
        ],
    ),
)
def test_reports_filename(func: Callable, a: int, b: int | str, string: int, name: str, correct: list) -> None:
    func(a, b)
    with open(name, "r", encoding="utf8") as f:
        test_list = []
        for i in f:
            test_list.append(i.strip())
        test_list = test_list[-string:]
        assert test_list == correct
