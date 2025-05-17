import inspect


def strict(func):
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        for name, value in bound.arguments.items():
            if name in func.__annotations__:
                expected_type = func.__annotations__[name]
                if not isinstance(value, expected_type):
                    raise TypeError(f"Argument '{name}' must be {expected_type.__name__}, got {type(value).__name__}")
        result = func(*args, **kwargs)

        if 'return' in func.__annotations__:
            expected_ret = func.__annotations__['return']
            if not isinstance(result, expected_ret):
                raise TypeError(f"Return value must be {expected_ret.__name__}, got {type(result).__name__}")
        return result

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b
