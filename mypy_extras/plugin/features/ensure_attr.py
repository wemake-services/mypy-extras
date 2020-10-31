from typing import ClassVar

from mypy.plugin import FunctionContext, Plugin
from mypy.types import Type as MypyType
from mypy.nodes import NameExpr
from typing_extensions import final


@final
class EnsureAttr(object):
    """Checks that a string is contained in a passed type."""

    _error_text: ClassVar[str] = 'Property "{0}" does not exist on type "{1}"'

    def __init__(self, plugin: Plugin, fullname: str) -> None:
        """We don't actually need this plugin here."""
        self._plugin = plugin   # TODO: create a base class for all plugins
        self._fullname = fullname

    def __call__(self, ctx: FunctionContext) -> MypyType:
        """Main plugin entrypoint."""
        attribute = ctx.api.expr_checker.accept(ctx.args[1][0])  # type: ignore
        literal = attribute.last_known_value

        if not literal or not isinstance(literal.value, str):
            return ctx.default_return_type

        assert isinstance(ctx.args[0][0], NameExpr)
        assert ctx.args[0][0].fullname
        defn = self._plugin.lookup_fully_qualified(ctx.args[0][0].fullname)

        assert defn and defn.node
        if defn.node.names.get(literal.value) is None:  # type: ignore
            msg = self._error_text.format(literal.value, defn.fullname)
            ctx.api.fail(msg, ctx.context)
        return literal
