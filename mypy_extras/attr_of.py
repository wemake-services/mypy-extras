from typing import Generic, Type, TypeVar

from typing_extensions import final

_ObjectType = TypeVar('_ObjectType')
_AttrQueryType = TypeVar('_AttrQueryType', bound=str)


@final
class AttrOf(Generic[_ObjectType, _AttrQueryType]):
    """
    Type to return specified attribute of other type.

    .. code:: python

      >>> from typing_extensions import Literal
      >>> from mypy_extras import AttrOf

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

    Does not exist in runtime.
    """


def ensure_attr(
    container: Type[_ObjectType],
    attribute: str,
) -> str:
    """
    Type to ensure that a string attribute belongs to a given type.

    This is how it works:

    .. code:: python

      >>> from mypy_extras import ensure_attr

      >>> class User(object):
      ...     email: str

      >>> assert {  # typechecks!
      ...     ensure_attr(User, 'email'): 'mail@example.com',
      ... } == {'email': 'mail@example.com'}

      >>> assert {  # typecheck fails!
      ...     ensure_attr(User, 'address'): 'Some street 12',
      ... } == {'address': 'Some street 12'}
      >>> # error: Property "address" does not exist on type "User"

    Does nothing in runtime.
    """
    return attribute
