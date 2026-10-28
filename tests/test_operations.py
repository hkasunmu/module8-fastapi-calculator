"""Unit tests for every function defined in operations.py."""

import pytest
from operations import add, divide, multiply, power, root, subtract


def test_add():
    assert add(2, 3) == 5
    assert add(-2, 2) == 0


def test_subtract():
    assert subtract(10, 4) == 6
    assert subtract(2, 5) == -3


def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(-3, 4) == -12


def test_divide():
    assert divide(12, 3) == 4
    assert divide(7, 2) == 3.5


def test_divide_by_zero():
    with pytest.raises(ValueError, match="divide by zero"):
        divide(5, 0)


def test_power():
    assert power(2.0, 3.0) == 8
    assert power(4.0, 0.5) == 2


def test_power_invalid():
    with pytest.raises(ValueError):
        power(-4.0, 0.5)
    with pytest.raises(ValueError):
        power(0.0, -1.0)


def test_root():
    assert root(27.0, 3.0) == pytest.approx(3)
    assert root(16.0, 2.0) == 4
    assert root(-27.0, 3.0) == pytest.approx(-3)


def test_root_invalid():
    with pytest.raises(ValueError, match="degree cannot be zero"):
        root(16.0, 0.0)
    with pytest.raises(ValueError, match="odd integer"):
        root(-16.0, 2.0)
    with pytest.raises(ValueError):
        root(0.0, -2.0)
