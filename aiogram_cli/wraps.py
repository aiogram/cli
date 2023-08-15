import asyncio
from typing import Callable, ParamSpec, TypeVar

W = ParamSpec("W")
T = TypeVar("T")


def async_command(func: Callable[W, T]) -> Callable[W, T]:
    def _wrap_async(*args: W.args, **kwargs: W.kwargs) -> T:
        return asyncio.run(func(*args, **kwargs))

    return _wrap_async
