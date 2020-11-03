from mypy.nodes import Decorator, FuncBase, Node, Var
from mypy.plugin import AnalyzeTypeContext, Plugin
from mypy.typeops import bind_self
from mypy.types import AnyType, FunctionLike, LiteralType
from mypy.types import Type as MypyType
from mypy.types import TypeOfAny, Instance
from mypy.expandtype import expand_type_by_instance
from typing_extensions import final

from mypy_extras.plugin.typeops.definitions import get_definition


@final
class AttrOf(object):
    """
    Plugin to analyze ``AttrOf[str, Literal['split']]`` notation.

    Basically, we fetch the value from names,
    then modify it if required and return to the user.

    We fallback to ``Any`` if anything goes wrong.
    """

    def __init__(self, plugin: Plugin, fullname: str) -> None:
        """We don't actually need anything from ``Plugin`` type here."""
        self._plugin = plugin
        self._fullname = fullname
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

        node = get_definition(typ, arg.value)
        if node is None:
            return self._fallback

        return self._process_type(
            self._process_class_node(node),
            typ,
            ctx,
        )

    def _process_class_node(self, node: Node) -> MypyType:
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

    def _process_type(
        self,
        template: MypyType,
        original: MypyType,
        ctx: AnalyzeTypeContext,
    ) -> MypyType:
        if isinstance(original, Instance):
            template = expand_type_by_instance(template, original)
        return ctx.api.analyze_type(template)
