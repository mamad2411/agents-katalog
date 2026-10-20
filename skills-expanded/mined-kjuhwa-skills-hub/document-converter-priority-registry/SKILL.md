---
name: document-converter-priority-registry
description: Pluggable converter registry where each candidate declares a numeric priority, registrations are prepended, and dispatch re-sorts stably per call so the most recently registered converter at a priority wins.
category: architecture
version: 1.0.0
tags: [architecture, registry, dispatch, plugin, priority, python]
source_type: extracted-from-git
source_url: https://github.com/microsoft/markitdown.git
source_ref: main
source_commit: 604bba13da2f43b756b49122cb65bdedb85b1dff
source_project: markitdown
source_path: packages/markitdown/src/markitdown/_markitdown.py
imported_at: 2026-04-18T00:00:00Z
confidence: medium
version_origin: extracted
---

# Document Converter Priority Registry

Generic pluggable-dispatch pattern: a host owns an ordered list of `(converter, priority)` registrations and picks one per request by (a) sorting stably by priority, (b) walking the sorted list, (c) asking each one "can you handle this?" (`accepts()`), and (d) calling `convert()` on the first that says yes. New registrations are `insert(0, ...)` so, at equal priority, **the most recently registered wins** — giving late-loaded plugins a way to shadow a built-in without changing core code.

## When to use

- You have a polymorphic handler contract (parser, converter, serializer, router).
- Built-in implementations must coexist with runtime-registered plugins.
- The order of tries matters: specific beats generic, newer beats older at the same priority.
- Priorities are fixed per converter but may change between calls (re-sort each call).

## The shape

```python
from dataclasses import dataclass
from typing import List

PRIORITY_SPECIFIC_FILE_FORMAT = 0.0   # specific: PDF, DOCX, Wikipedia
PRIORITY_GENERIC_FILE_FORMAT  = 10.0  # catch-all: text/*, html

@dataclass(kw_only=True, frozen=True)
class ConverterRegistration:
    converter: "DocumentConverter"
    priority: float

class Host:
    def __init__(self):
        self._converters: List[ConverterRegistration] = []

    def register_converter(self, converter, *, priority: float = PRIORITY_SPECIFIC_FILE_FORMAT):
        # insert at index 0 so later registrations win stable-sort ties
        self._converters.insert(0, ConverterRegistration(converter=converter, priority=priority))

    def dispatch(self, *args, **kwargs):
        # Re-sort on every call — priorities may change between calls.
        # `sorted` is stable → same-priority entries keep insertion order.
        for reg in sorted(self._converters, key=lambda r: r.priority):
            if reg.converter.accepts(*args, **kwargs):
                return reg.converter.convert(*args, **kwargs)
```

## Why these three choices

1. **Lower priority value = tried first.** Counter-intuitive, but useful: "specific format" = priority 0, "generic catch-all" = priority 10. New plugins can pick any float to slot themselves in. Document this loudly to avoid confusion.
2. **Insert at head + stable sort.** Equal-priority registrations preserve insertion order, and the most-recent insertion lands at the front of the tie-group. Plugins can override built-ins without extra API.
3. **Re-sort per call.** Priorities are rare to change, but cheap to re-sort (N is small). Avoids a stale-cache bug class if a converter exposes a mutable priority.

## Plugin override in practice

Built-in registrations (all priority 0 except the three generic ones at 10):

```python
self.register_converter(PlainTextConverter(), priority=10.0)   # generic
self.register_converter(HtmlConverter(),      priority=10.0)   # generic
self.register_converter(PdfConverter())                         # specific, p=0
self.register_converter(DocxConverter())                        # specific, p=0
# ...
```

A plugin then shadows the PDF handler by simply doing:

```python
host.register_converter(MyPdfConverter())   # also priority 0 → now at head of tie group → wins
```

No introspection, no unregister step, no plugin lifecycle API.

## Plugin loader glue

Load plugins via `importlib.metadata.entry_points`, wrap each in try/except so a broken plugin doesn't kill the host:

```python
from importlib.metadata import entry_points
for ep in entry_points(group="markitdown.plugin"):
    try:
        plugin = ep.load()
        plugin.register_converters(host)
    except Exception:
        warn(f"Plugin '{ep.name}' failed to load ... skipping:\n{traceback.format_exc()}")
```

See companion skill `python-entrypoint-plugin-loader` for the full pattern.

## Anti-patterns

- **Using a `dict[str, Converter]` by extension.** Collapses plugin override, forces one-handler-per-extension, can't encode "try these in order."
- **Reversed priority (higher = first).** You'll save ten minutes on read-intuition but lose hours when a plugin author picks the wrong sign and their handler never runs. Pick one convention and document it.
- **Single sorted list, no re-sort.** Subtle bug: if any converter exposes a settable priority, your cached sort goes stale.
- **`append()` instead of `insert(0)`.** At equal priority you now favor the *oldest* registration, which is the opposite of what plugin authors expect.

## Variations

- **Multi-hit dispatch.** For "chain of responsibility where every responder must run," iterate without `break` — still uses the same sorted list.
- **Failover.** If `convert()` raises a retriable error, record it and fall through to the next converter (markitdown does this; see companion skill `accepts-then-convert-two-phase-dispatch`).
- **Multiple guesses.** If the request's signal (e.g., mimetype) is ambiguous, iterate over multiple input guesses in an outer loop and the sorted converter list in an inner loop.
