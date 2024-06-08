from . import expression as expr


class MalformedExpression(Exception): ...


class InvalidToken(Exception): ...


OPERATORS = {"+": expr.Add, "*": expr.Mult, "-": expr.Sub, "/": expr.Div}


def get_number(s: str) -> expr.Number:
    return expr.Number(float(s))


def get_operator(s: str) -> expr.Operator:
    return OPERATORS[s]()


def tokenize(whole_str: str) -> list[expr.Token]:
    """Take a string and returns a list of Token."""

    def process_token(s: str) -> expr.Token:
        if s.replace(".", "", 1).isnumeric():
            return get_number(s)
        elif s in OPERATORS:
            return get_operator(s)
        else:
            raise InvalidToken(f"{s} is invalid")

    return [process_token(token) for token in whole_str.strip().split()]


def reduce_ops(
    tokens: list[expr.Token], operators: tuple[type[expr.Operator], ...] | None = None
) -> list[expr.Token]:
    """Takes a list of tokens and returns a new list where operations involving
    operators given in operators tuple are evaluated. If operators is empty
    evaluates all operations.
    """
    operators = operators or tuple(OPERATORS.values())
    if not tokens:
        return tokens
    result = [tokens[0]]
    for i in range(1, len(tokens), 2):
        op = tokens[i]
        try:
            right = tokens[i + 1]
        except IndexError:
            raise MalformedExpression()
        if any(isinstance(op, operator) for operator in operators):
            left = result.pop()
            if not isinstance(left, expr.Expression) or not isinstance(
                right, expr.Expression
            ):
                raise MalformedExpression()
            result.append(expr.Number(op.eval(left, right)))  # type: ignore
        else:
            result.append(op)
            result.append(right)
    return result


def parse_string(whole_str: str) -> expr.Expression:
    """Takes a string and returns an Expression. If the first operand is missing
    in the string it will be replaced with 0. Therefore an empty string is
    evaluated to 0.
    """
    tokens = tokenize(whole_str)
    if not tokens:
        return expr.Expression()
    if not isinstance(tokens[0], expr.Expression):
        tokens.insert(0, expr.Expression())
    tokens = reduce_ops(tokens, (expr.Mult, expr.Div))
    tokens = reduce_ops(tokens)
    if not len(tokens) == 1:
        raise MalformedExpression()
    else:
        if isinstance(tokens[0], expr.Expression):
            return tokens.pop(0)  # type: ignore
        else:
            raise MalformedExpression()
