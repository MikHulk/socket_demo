class Token:
    """Represents any element of an arithmetic expression. A number, an operator
    or a sub-expression.
    """


class Expression(Token):
    """An expression represents something which able to produce a result.
    Namely a number or an arithmetic expression.
    """

    @property
    def result(self) -> float:
        return 0


class Operator(Token):
    """Represents an operator. This is an abstract class which must be specialized,
    implementing the compute_result method."""

    def compute_result(self, left: Expression, right: Expression) -> float:
        raise NotImplementedError()

    def eval(self, left: Expression, right: Expression) -> float:
        """Take left and right operands and return the result as a float."""
        return self.compute_result(left, right)


class Add(Operator):
    """Represents the addition operator."""

    def compute_result(self, left, right):
        return left.result + right.result


class Mult(Operator):
    """Represents the multiplication operator."""

    def compute_result(self, left, right):
        return left.result * right.result


class Sub(Operator):
    """Represents the substraction operator."""

    def compute_result(self, left, right):
        return left.result - right.result


class Div(Operator):
    """Represents the division operator."""

    def compute_result(self, left, right):
        return left.result / right.result


class Operation(Expression):
    """Represents an arithmetic operation. The result is evaluated only when
    the property is called.
    """

    def __init__(self, left: Expression, right: Expression, op: Operator):
        self.left = left
        self.right = right
        self.op = op

    @property
    def result(self) -> float:
        return self.op.eval(self.left, self.right)


class Number(Expression):
    """Represents a number."""

    def __init__(self, value: float):
        self.value = value

    @property
    def result(self) -> float:
        return self.value
