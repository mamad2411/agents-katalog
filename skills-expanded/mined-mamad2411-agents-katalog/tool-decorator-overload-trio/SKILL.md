---
name: tool-decorator-overload-trio
description: A `@tool` decorator that handles three calling conventions — bare on a function, parameterized on a function, and as a no-op on a BaseTool — using three @overload stubs so type checkers infer correctly in every case.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [decorator, typing, overload, agent-tools]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/tools/tool_decorator.py
imported_at: 2026-04-18T00:00:00Z
---

# Tool Decorator with Three Typing Overloads

## When to use
Your `@tool` decorator must support `@tool`, `@tool(name="x", ...)`, and applying to a `BaseTool` subclass without losing type information. Three `@overload` stubs cover each case so users get correct IDE hints regardless of usage shape.

## How it works
- Three `@overload` stubs declare the three signatures (BaseTool path, function path, parameterized factory path).
- The runtime implementation reads `func` first; if `None`, returns a wrapper closure (factory pattern); if `BaseTool`, attaches the registered-tool marker idempotently; otherwise registers as a function tool.
- `should_register_function()` checks whether any registration metadata was provided so a bare `@tool` on an undecorated function remains a no-op (backwards compatibility for legacy code).

## Example
```python
@overload
def tool(func: BaseTool, *, name=None, ...) -> BaseTool: ...
@overload
def tool(func: F, *, name=None, ...) -> F: ...
@overload
def tool(func: None = None, *, name=None, ...) -> Callable[[F], F]: ...

def tool(func=None, *, name=None, description=None, input_schema=None,
         source=None, surfaces=None, ...) -> Any:
    def should_register_function() -> bool:
        return any([name is not None, description is not None, ...])

    def attach(target):
        if isinstance(target, BaseTool):
            if surfaces is not None:
                setattr(target, REGISTERED_TOOL_ATTR,
                        RegisteredTool.from_base_tool(target, surfaces=surfaces))
            return target
        if should_register_function():
            setattr(target, REGISTERED_TOOL_ATTR,
                    RegisteredTool.from_function(target, name=name, ...))
        return target

    if func is None:
        return lambda inner: attach(inner)   # parameterized form
    return attach(func)                      # bare form
```

## Gotchas
- The middle overload (`func: F, *, ...`) needs `# noqa: UP047` on Python <3.13 because of how `TypeVar` interacts with overload narrowing.
- Keep the marker attribute name distinctive (`__opensre_registered_tool__`) to avoid collisions with other libraries that might decorate the same function.
- The "bare-with-no-metadata is no-op" branch is critical for migration from older codebases where `@tool` was used as a documentation hint only.
