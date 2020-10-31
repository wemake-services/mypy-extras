from typing import Callable, Mapping, Optional, Type

from mypy.plugin import AnalyzeTypeContext, Plugin
from mypy.types import Type as MypyType
from typing_extensions import final

from mypy_extras.plugin.features import attr_of

_TypeAnalyzeHook = Callable[
    [Plugin],
    Callable[[AnalyzeTypeContext], MypyType],
]


@final
class _MypyExtrasPlugin(Plugin):
    _type_analyze: Mapping[str, _TypeAnalyzeHook] = {
        'mypy_extras.attr_of.AttrOf': attr_of.AttrOf,
    }

    def get_type_analyze_hook(
        self,
        fullname: str,
    ) -> Optional[Callable[[AnalyzeTypeContext], MypyType]]:
        hook = self._type_analyze.get(fullname)
        if hook is not None:
            return hook(self)
        return None


def plugin(version: str) -> Type[Plugin]:
    """Plugin's public API and entrypoint."""
    return _MypyExtrasPlugin
