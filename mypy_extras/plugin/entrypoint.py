from typing import Callable, Mapping, Optional, Type

from mypy.plugin import AnalyzeTypeContext, FunctionContext, Plugin
from mypy.types import Type as MypyType
from typing_extensions import final

from mypy_extras.plugin.features import attr_of, ensure_attr

#: Used for `get_type_analyze_hook`:
_TypeAnalyzeHook = Callable[
    [Plugin],
    Callable[[AnalyzeTypeContext], MypyType],
]

#: Used for `get_function_hook`:
_FunctionAnalyzeHook = Callable[
    [Plugin],
    Callable[[FunctionContext], MypyType],
]


@final
class _MypyExtrasPlugin(Plugin):
    """"""

    _type_analyze: Mapping[str, _TypeAnalyzeHook] = {
        'mypy_extras.attr_of.AttrOf': attr_of.AttrOf,
    }

    _functions: Mapping[str, _FunctionAnalyzeHook] = {
        'mypy_extras.attr_of.ensure_attr': ensure_attr.EnsureAttr,
    }

    def get_type_analyze_hook(
        self,
        fullname: str,
    ) -> Optional[Callable[[AnalyzeTypeContext], MypyType]]:
        hook = self._type_analyze.get(fullname)
        if hook is not None:
            return hook(self)
        return None

    def get_function_hook(
        self,
        fullname: str,
    ) -> Optional[Callable[[FunctionContext], MypyType]]:
        hook = self._functions.get(fullname)
        if hook is not None:
            return hook(self)
        return None


def plugin(version: str) -> Type[Plugin]:
    """Plugin's public API and entrypoint."""
    return _MypyExtrasPlugin
