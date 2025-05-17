import pytest
from task1.solution import sum_two, strict


def test_sum_two_valid():
    assert sum_two(1, 2) == 3


def test_sum_two_invalid_arg_type():
    with pytest.raises(TypeError) as exc_info:
        sum_two(1, 2.4)
    assert "Argument 'b' must be int" in str(exc_info.value)


def test_sum_two_invalid_return_type():
    @strict
    def f(a: int, b: int) -> str:
        return a + b  # returns int instead of str

    with pytest.raises(TypeError) as exc_info:
        f(1, 2)
    assert "Return value must be str" in str(exc_info.value)
