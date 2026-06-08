import pytest
from pydantic import BaseModel

from atlas.tools import Tool, ToolRegistry


class AddArgs(BaseModel):
    a: int
    b: int


def _add(a: int, b: int) -> int:
    return a + b


def _make_tool() -> Tool:
    return Tool(name="add", description="add two ints", args_schema=AddArgs, func=_add)


def test_tool_validates_and_invokes():
    tool = _make_tool()
    assert tool.invoke(a=2, b=3) == 5


def test_registry_lookup_and_duplicate_guard():
    reg = ToolRegistry()
    reg.register(_make_tool())
    assert reg.names() == ["add"]
    assert reg.get("add").invoke(a=1, b=1) == 2
    with pytest.raises(ValueError):
        reg.register(_make_tool())
    with pytest.raises(KeyError):
        reg.get("missing")
