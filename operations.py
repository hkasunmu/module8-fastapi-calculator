"""Arithmetic operations for the FastAPI calculator."""

import math


def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return a minus b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return a divided by b; reject division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(a: float, b: float) -> float:
    """Raise a to the power b; require a real, finite result."""
    if a == 0 and b < 0:
        raise ValueError("Zero cannot be raised to a negative power")
    if a < 0 and not float(b).is_integer():
        raise ValueError("Fractional powers of negative numbers are not real")
    try:
        result = a ** b
    except (OverflowError, ZeroDivisionError) as exc:
        raise ValueError("Result is outside the supported range") from exc
    if isinstance(result, complex) or not math.isfinite(result):
        raise ValueError("Result must be a finite real number")
    return float(result)


def root(a: float, b: float) -> float:
    """Return the b-th root of a; handle odd roots of negative numbers."""
    if b == 0:
        raise ValueError("Root degree cannot be zero")
    if a == 0 and b < 0:
        raise ValueError("Zero cannot have a negative-degree root")
    if a < 0:
        if not float(b).is_integer() or int(b) % 2 == 0:
            raise ValueError("Negative numbers require an odd integer root degree")
        return -((-a) ** (1 / b))
    try:
        result = a ** (1 / b)
    except (OverflowError, ZeroDivisionError) as exc:
        raise ValueError("Result is outside the supported range") from exc
    if not math.isfinite(result):
        raise ValueError("Result must be a finite real number")
    return result
