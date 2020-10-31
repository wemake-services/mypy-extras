from typing import Callable, TypeVar, cast

from mypy.types import AnyType, TypeOfAny

_FunctionType = TypeVar('_FunctionType', bound=Callable)  # type: ignore


def fallback_to_any(function: _FunctionType) -> _FunctionType:
    """
    Handles and swallows type errors in our plugin, returns ``Any`` instead.

    We have quite a lot of ``assert`` statements here and there.
    In some cases, we don't want them to raise warnings.
    """
    def decorator(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            return AnyType(TypeOfAny.from_error)
    return cast(_FunctionType, decorator)
