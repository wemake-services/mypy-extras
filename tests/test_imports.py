import pytest

from mypy_extras import AttrOf


@pytest.mark.parametrize('public_item', [
    AttrOf,
])
def test_imports(public_item) -> None:
    """Ensures that imported items do exist."""
    assert public_item
