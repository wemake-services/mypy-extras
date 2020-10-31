from typing import Generic, TypeVar

from typing_extensions import final

_ObjectType = TypeVar('_ObjectType')
_AttrQueryType = TypeVar('_AttrQueryType', bound=str)


@final
class AttrOf(Generic[_ObjectType, _AttrQueryType]):
    """
    Type to return specified attribute of other type.

    .. code:: python

      >>> from typing_extensions import Literal
      >>> from mypy_extras.types import AttrOf

      >>> def example() -> AttrOf[str, Literal['split']]:
      ...     return str.split

      >>> # note: Revealed type is
      >>> # 'def (
      >>> #      self: builtins.str,
      >>> #      sep: Union[builtins.str, None] =,
      >>> #      maxsplit: builtins.int =,
      >>> # ) -> builtins.list[builtins.str]'

    Make sure to only use ``Literal`` as attribute query.
    We fallback to any on any possible errors.

    We also do require ``mypy_extras`` plugin to be enabled in ``mypy``.

    """
