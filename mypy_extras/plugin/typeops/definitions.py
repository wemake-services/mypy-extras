from typing import Optional

from mypy.nodes import Node
from mypy.types import Instance
from mypy.types import Type as MypyType
from mypy.types import TypeType


def get_definition(typ: MypyType, arg: str) -> Optional[Node]:
    """Gets definition of a type from SymbolTableNode."""
    if isinstance(typ, Instance):  # TODO: support Union types
        return _get_defition_instance(typ, arg)
    elif isinstance(typ, TypeType):
        return _get_defition_type(typ, arg)
    return None


def _get_defition_instance(typ: Instance, arg: str) -> Optional[Node]:
    sym = typ.type.names.get(arg)
    return sym.node if sym is not None else None


def _get_defition_type(typ: TypeType, arg: str) -> Optional[Node]:
    if not isinstance(typ.item, Instance):
        return None  # it can be type var or union or etc

    sym = typ.item.type.names.get(arg)  # TODO: support Union types
    return sym.node if sym is not None else None
