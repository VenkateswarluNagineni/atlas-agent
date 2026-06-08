"""Typed tool registry.

Agents call tools by name; the orchestrator looks them up here and validates arguments
against each tool's pydantic schema before invocation. Typed, validated tool calls are
what keeps a multi-agent system debuggable instead of a pile of free-form prompts.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from pydantic import BaseModel


class Tool(BaseModel):
    """A callable an agent may invoke, with a typed argument schema."""

    name: str
    description: str
    args_schema: type[BaseModel]
    func: Callable[..., Any]

    model_config = {"arbitrary_types_allowed": True}

    def invoke(self, **kwargs: Any) -> Any:
        """Validate ``kwargs`` against ``args_schema``, then run the tool."""
        validated = self.args_schema(**kwargs)
        return self.func(**validated.model_dump())


class ToolRegistry:
    """Name -> Tool lookup with duplicate protection."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise KeyError(f"unknown tool: {name}")
        return self._tools[name]

    def names(self) -> list[str]:
        return sorted(self._tools)
