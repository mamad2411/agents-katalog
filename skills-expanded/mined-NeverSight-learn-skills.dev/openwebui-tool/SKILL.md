---
name: openwebui-tool
description: Write and verify Open WebUI Python tools — the single-file `Tools` class pasted into Workspace > Tools. Use when creating, editing, or debugging an Open WebUI tool, its frontmatter, its Valves/UserValves, or its event emitters.
license: MIT
compatibility: Requires Python 3 to run scripts/check_tool.py
metadata:
  author: gdevenyi
  version: "1.0"
  open-webui-version: "0.10"
---

# Open WebUI Python tools

A tool is **one Python file**. Open WebUI `exec`s the file, instantiates `Tools()`, and turns
every public method into a function the model can call. That set of public methods is the
tool's **surface** — a helper you forgot to prefix with `_` is a function the model will call.

The docstring is not a comment. Its first block becomes the function description sent to the
model, and each `:param name:` line becomes a parameter description. The docstring is the prompt.

## The file

```python
"""
title: Package Lookup
author: you
description: Look up a package on PyPI
requirements: httpx
version: 0.1.0
licence: MIT
"""

import json
from typing import Any, Callable, Optional

import httpx
from pydantic import BaseModel, Field


class Tools:
    class Valves(BaseModel):
        base_url: str = Field(
            default="https://pypi.org/pypi",
            description="PyPI JSON API root",
        )

    class UserValves(BaseModel):
        include_yanked: bool = Field(default=False, description="Include yanked releases")

    def __init__(self):
        self.valves = self.Valves()

    async def get_package(
        self,
        name: str,
        version: Optional[str] = None,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Any]] = None,
    ) -> str:
        """
        Look up a Python package on PyPI and return its metadata.

        :param name: The package name, e.g. `httpx`
        :param version: A specific version; omit for the latest release
        :return: JSON with summary, latest version, homepage and licence
        """
        if __event_emitter__:
            await __event_emitter__(
                {"type": "status", "data": {"description": f"Fetching {name}...", "done": False}}
            )

        try:
            data = await self._fetch(name, version)
        except httpx.HTTPStatusError as e:
            return f"PyPI returned {e.response.status_code} for package '{name}'."
        except Exception as e:
            return f"Could not reach PyPI: {e}"

        info = data.get("info", {})
        return json.dumps(
            {"name": info.get("name"), "version": info.get("version"), "summary": info.get("summary")},
            ensure_ascii=False,
        )

    async def _fetch(self, name: str, version: Optional[str]) -> dict:
        path = f"{name}/{version}/json" if version else f"{name}/json"
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f"{self.valves.base_url}/{path}")
            response.raise_for_status()
            return response.json()
```

That file generates exactly this spec for the model — nothing else in the file is reachable:

```json
{"name": "get_package",
 "description": "Look up a Python package on PyPI and return its metadata.",
 "parameters": {"type": "object", "required": ["name"], "properties": {
   "name": {"type": "string", "description": "The package name, e.g. `httpx`"},
   "version": {"type": "string", "description": "A specific version; omit for the latest release"}}}}
```

## Rules the skeleton cannot show

- **Line 1 is exactly `"""`.** A comment, an import, or a blank line above it makes the whole
  frontmatter invisible — `requirements` then never installs, silently.
- **Keep helpers off the surface** with a leading `_`. Everything else public on `Tools` — including
  anything inherited — is a function the model can call.
- **reST docstrings only.** `:param name: text` reaches the model; a Google-style `Args:` block
  reaches nothing.
- **Type-hint every model-facing parameter.** The hints generate the JSON schema. Hints must resolve
  at import time; an unresolvable annotation makes saving the tool fail outright.
- **Give every injected `__dunder__` parameter a default.** Open WebUI supplies them only where it
  has them, and the model never sees them — they are stripped from the schema.
- **`__init__` takes no arguments and sets `self.valves = self.Valves()`.** Without that line the
  admin's configured valve values are dropped on the floor.
- **Every method `async def`.** A sync method runs inline on the event loop and blocks the server;
  push blocking work through `await asyncio.to_thread(...)`.
- **Return a string** (a `dict` or `list` is JSON-dumped for you). Return a readable error message
  rather than raising — a raised exception reaches the model as its bare `str()`.
- **Progress goes through `status` events; the answer goes through the return value.** The four
  content events (`message`, `chat:message`, `chat:message:delta`, `replace`) are overwritten by
  completion snapshots under Native mode, which is the only supported mode.

## Verify

```
python scripts/check_tool.py mytool.py
```

The script is stdlib-only, but it executes the tool file, so the tool's own imports must resolve —
`uv run --with httpx --with pydantic python scripts/check_tool.py mytool.py` for the file above.

It reproduces the server's load and spec generation. Two bars, both must hold: it exits clean, and
every name in the printed **tool surface** is one you meant the model to call.

Then paste the file into Workspace > Tools. The tool id is set there, not in the file, and must be a
lowercase Python identifier.

## Reference

Read [`references/REFERENCE.md`](references/REFERENCE.md) for the full injected-parameter list, the event-emitter
catalogue (`status`, `citation`, `notification`, `confirmation`, `input`, files), valve input types
(password, select, multiselect, dynamic options), returning files or embedded HTML, and the
inherited flags that no longer do anything.
