from mypy.nodes import Decorator, FuncBase, Node, Var
from mypy.plugin import AnalyzeTypeContext, Plugin
from mypy.typeops import bind_self
from mypy.types import AnyType, FunctionLike, Instance, LiteralType
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny, TypeType
from typing_extensions import final


@final
class AttrOf(object):
    """
    Plugin to analyze ``AttrOf[str, Literal['split']]`` notation.

    Basically, we fetch the value from names,
    then modify it if required and return to the user.

    We fallback to ``Any`` if anything goes wrong.
    """

    def __init__(self, plugin: Plugin) -> None:
        """We don't actually need anything from ``Plugin`` type here."""
        self._plugin = plugin
        self._fallback = AnyType(TypeOfAny.from_error)

    def __call__(self, ctx: AnalyzeTypeContext) -> MypyType:
        """Main plugin entrypoint."""
        typ = ctx.api.analyze_type(ctx.type.args[0])
        arg = ctx.api.analyze_type(ctx.type.args[1])

        if not isinstance(arg, LiteralType) or not isinstance(arg.value, str):
            ctx.api.fail(
                'The second argument must be a string literal',
                ctx.context,
            )
            return self._fallback

        node = self._extract_node(typ, arg.value)
        if node is None:
            return self._fallback

        return ctx.api.analyze_type(self._process_node_type(node))

    def _extract_node(self, typ: MypyType, arg: str) -> Node:
        if isinstance(typ, Instance):
            sym = typ.type.names.get(arg)
            return sym.node if sym is not None else None
        elif isinstance(typ, TypeType):
            sym = typ.item.type.names.get(arg)
            return sym.node if sym is not None else None
        return None

    def _process_node_type(self, node: Node) -> MypyType:
        if isinstance(node, Decorator):
            if not node.func.is_static:
                assert isinstance(node.func.type, FunctionLike)
                return bind_self(
                    node.func.type,
                    is_classmethod=node.func.is_class,
                )

            assert node.func.type
            return node.func.type
        elif isinstance(node, FuncBase):
            assert isinstance(node.type, FunctionLike)
            return bind_self(node.type, is_classmethod=False)

        assert isinstance(node, Var)
        assert node.type
        return node.type
