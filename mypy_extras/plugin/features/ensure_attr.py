from typing import ClassVar

from mypy.plugin import FunctionContext, Plugin
from mypy.types import Type as MypyType
from typing_extensions import final

from mypy_extras.plugin.typeops.definitions import get_definition


@final
class EnsureAttr(object):
    """Checks that a string is contained in a passed type."""

    _error_text: ClassVar[str] = 'Property "{0}" does not exist on type "{1}"'

    def __init__(self, plugin: Plugin) -> None:
        """We don't actually need this plugin here."""
        self._plugin = plugin   # TODO: create a base class for all plugins

    def __call__(self, ctx: FunctionContext) -> MypyType:
        """Main plugin entrypoint."""
        container = ctx.api.expr_checker.accept(ctx.args[0][0])
        attribute = ctx.api.expr_checker.accept(ctx.args[1][0])

        defn = get_definition(
            container.ret_type,
            attribute.last_known_value.value,
        )
        if defn is None:
            ctx.api.fail(self._error_text.format(
                attribute.last_known_value.value,
                container.ret_type,
            ), ctx.context)
        return attribute
