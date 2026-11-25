---
name: tool-registry-discovery-from-modules
description: Auto-discover all agent tools by walking a package, importing each module, and collecting any object marked with a registration attribute or any BaseTool subclass — with skip lists, deduping, and surface filtering ("investigation" vs "chat").
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [tools, registry, discovery, plugin, agent]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/tools/registry.py
imported_at: 2026-04-18T00:00:00Z
---

# Tool Registry: Auto-Discover from Package

## When to use
You have dozens or hundreds of agent tools (one per file or one per class) and you don't want a hand-maintained `__all__` registry. Tools should be picked up at import time, deduped by name, and filtered by "surface" (which interface gets to see them) so the same code can serve a chat agent and an investigation pipeline.

## How it works
- `pkgutil.iter_modules(tools_package.__path__)` enumerates every submodule of `app.tools`.
- A skip-set (`base`, `registry`, `registered_tool`, `tool_decorator`, `utils`, ...) excludes infrastructure modules.
- For each module, `inspect.getmembers` looks for any object with the `__opensre_registered_tool__` marker (the decorator's footprint) or any `BaseTool` instance/subclass.
- Duplicates by tool name are detected and a warning logged; first wins.
- A single `@lru_cache` snapshot caches the result; `clear_tool_registry_cache()` resets for hot-reload tests.
- A separate `_LEGACY_CHAT_TOOL_NAMES` set provides a backwards-compatible mapping from "this tool also appears on the chat surface" without forcing every tool to declare its surfaces explicitly.

## Example
```python
import importlib, inspect, pkgutil
from functools import lru_cache

@lru_cache(maxsize=1)
def _load_registry_snapshot():
    tools_by_name = {}
    for module_info in pkgutil.iter_modules(tools_package.__path__):
        if module_info.name in _SKIP_MODULE_NAMES:
            continue
        try:
            module = importlib.import_module(f"{tools_package.__name__}.{module_info.name}")
        except Exception as exc:
            logger.warning("[tools] Skipping %s: %s", module_info.name, exc)
            continue
        for tool in _collect_registered_tools_from_module(module):
            if tool.name not in tools_by_name:
                tools_by_name[tool.name] = tool
            else:
                logger.warning("[tools] Duplicate tool '%s'; keeping first", tool.name)
    return tuple(sorted(tools_by_name.values(), key=lambda t: t.name))

def get_registered_tools(surface=None):
    tools = list(_load_registry_snapshot())
    return [t for t in tools if surface is None or surface in t.surfaces]

def clear_tool_registry_cache():
    _load_registry_snapshot.cache_clear()
```

## Gotchas
- Catch `ModuleNotFoundError` separately from generic `Exception` so optional dependencies (e.g. `confluent-kafka` for the Kafka tool) silently skip rather than crash discovery.
- `_candidate_belongs_to_module(candidate, module_name)` filter prevents pulling in re-exported classes from other modules.
- Use `id(candidate)` to dedupe class vs instance double-counts within one module.
- The skip list also needs `*_test` suffixes to avoid importing test fixtures during prod startup.
