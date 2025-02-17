import pytest
from prak28 import evaluateExpression


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("2+3", "5"),
        ("10-5", "5"),
        ("6*7", "42"),
        ("8/2", "4.0"),
        ("10//3", "3"),
        ("10%3", "1"),
    ],
)
def test_operations(expression, expected):
    assert evaluateExpression(expression) == expected
