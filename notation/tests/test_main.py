import pytest
from prefixToInfix.main import prefix_to_infix

@pytest.mark.parametrize("expression, expected", [
    ("+ 1 2", "(1 + 2)"),
    ("- 10 3", "(10 - 3)"),
    ("* 5 5", "(5 * 5)"),
    ("/ 16 4", "(16 / 4)"),
    ("+ 5 * 4 45", "(5 + (4 * 45))"),
    ("- + 2 3 4", "((2 + 3) - 4)"),
    ("* + 1 2 3", "((1 + 2) * 3)"),
    ("/ 9 * 2 3", "(9 / (2 * 3))"),
])
def test_prefix_to_infix(expression, expected):
    assert prefix_to_infix(expression) == expected

@pytest.mark.parametrize("expression", [
    "+ 123",
    "* 56 x",
    "- 5 12 4",
    "- + *",
    "/ 7",
    "+ 1 2 3",
])
def test_prefix_to_infix_errors(expression):
    with pytest.raises(ValueError):
        prefix_to_infix(expression)
