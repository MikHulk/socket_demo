import pytest

from ..parser import parse_string, tokenize, MalformedExpression, InvalidToken
from .. import expression as expr


def test_tokenize():
    tokens = tokenize("")
    assert len(tokens) == 0

    tokens = tokenize("2")
    assert len(tokens) == 1
    assert tokens[0].result == 2

    tokens = tokenize("2 + 3")
    assert len(tokens) == 3
    assert tokens[0].result == 2
    assert tokens[2].result == 3
    assert tokens[1].eval(tokens[0], tokens[2]) == 5

    tokens = tokenize("+ 3")
    assert len(tokens) == 2
    assert type(tokens[0]) is expr.Add
    assert tokens[1].result == 3

    tokens = tokenize("- 3")
    assert len(tokens) == 2
    assert type(tokens[0]) is expr.Sub
    assert tokens[1].result == 3

    tokens = tokenize("3 * 6 - 3 * 2")
    assert len(tokens) == 7
    assert tokens[0].result == 3
    assert tokens[2].result == 6
    assert tokens[4].result == 3
    assert tokens[6].result == 2
    left = tokens[1].eval(tokens[0], tokens[2])
    assert left == 18
    right = tokens[5].eval(tokens[4], tokens[6])
    assert right == 6
    assert tokens[3].eval(expr.Number(left), expr.Number(right)) == 12


def test_no_op_return_zero():
    expression = parse_string("")
    assert expression.result == 0


def test_simple_addition():
    expression = parse_string("2 + 3")
    assert expression.result == 5


def test_simple_multiplication():
    expression = parse_string("2 * 3")
    assert expression.result == 6


def test_simple_division():
    expression = parse_string("10 / 5")
    assert expression.result == 2


def test_simple_substraction():
    expression = parse_string("2 - 3")
    assert expression.result == -1


def test_expressions_with_float():
    expression = parse_string("2.2 * 3 + 5.4")
    assert expression.result == 12


def test_complex_expressions():
    expression = parse_string("2 * 3 + 5")
    assert expression.result == 11
    expression = parse_string("2 + 3 * 5")
    assert expression.result == 17
    expression = parse_string("6 * 2 + 3 * 5")
    assert expression.result == 27
    expression = parse_string("6 + 2 * 3 + 5")
    assert expression.result == 17
    expression = parse_string("6 + 2 * 3 + 4 / 4")
    assert expression.result == 13
    expression = parse_string("- 6 + 2 * 3 + 4 / 4")
    assert expression.result == 1
    expression = parse_string("- 8 + 2 * 3 + 4 / 4")
    assert expression.result == -1
    expression = parse_string("- 7 + 2 * 3 + 4 / 4")
    assert expression.result == 0
    expression = parse_string("4 / 6 + 2 * 3 + 4 / 4")
    assert expression.result == 4 / 6 + 2 * 3 + 4 / 4


def test_ill_expressions():
    with pytest.raises(MalformedExpression):
        parse_string("2 * * 3 + 5")
    with pytest.raises(MalformedExpression):
        parse_string("2 * 3 +")
    with pytest.raises(MalformedExpression):
        parse_string("2 3 5 6 43")
    with pytest.raises(MalformedExpression):
        parse_string("2 3 5 6 43 + - -")


def test_expressions_with_invalid_token():
    with pytest.raises(InvalidToken):
        parse_string("5 !")
    with pytest.raises(InvalidToken):
        parse_string("5 factorial")
    with pytest.raises(InvalidToken):
        parse_string("kikou 456")
    with pytest.raises(InvalidToken):
        parse_string("2+456")
