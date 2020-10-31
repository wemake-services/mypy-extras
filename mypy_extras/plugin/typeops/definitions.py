from typing import Optional

from mypy.nodes import Node
from mypy.types import Instance
from mypy.types import Type as MypyType
from mypy.types import TypeType


def get_definition(typ: MypyType, arg: str) -> Optional[Node]:
    """"""
    if isinstance(typ, Instance):  # TODO: support Union types
        sym = typ.type.names.get(arg)
        return sym.node if sym is not None else None
    elif isinstance(typ, TypeType):
        if not isinstance(typ.item, Instance):
            return None  # it can be type var or union or etc

        sym = typ.item.type.names.get(arg)  # TODO: support Union types
        return sym.node if sym is not None else None
    return None
