---
name: context-setup
description: Guides correct setup of pydita's DitaContext for a DITA processing pipeline. Use this skill when you need to wire together resolveMap(), KeyspaceManager, DitavalFilter, and DitaContext, or when a pipeline is failing because of incorrect initialisation order, missing DITA-OT configuration, or a mismatched errors dictionary.
compatibility: Python 3.10+. Requires pydita (lxml, anytree, aenum). A DITA Open Toolkit installation is needed for DTD-aware parsing (set DITA_OT_DIR or dita.ot.dir in ~/.build.properties).
---

## Overview

`DitaContext` is pydita's central processing object. It bundles:
- a `KeyspaceManager` (key spaces built from the resolved map)
- a `DitavalFilter` (conditional filtering)
- a shared `errors` dict (error accumulation across all pydita calls)
- an optional `mapContext` element (current position in the map tree)

**Initialisation must follow a strict order** — every step depends on the output of the previous one.

---

## Canonical setup pattern

```python
from pydita import resolvemap, xmlutils
from pydita.ditaval import DitavalFilter
from pydita.keyspacemgr import KeyspaceManager
from pydita.ditacontext import DitaContext

# 1. Shared error collector (pass the same dict everywhere)
errors: dict = {}

# 2. Optionally load a DITAVAL filter
ditaval_filter = DitavalFilter(errors=errors)
# — or load from a file (pass a list of paths):
# ditaval_filter = DitavalFilter(ditavalFiles=["path/to/filter.ditaval"], errors=errors)

# 3. Resolve the root map (flattens the map tree into a single document)
resolved_map = resolvemap.resolveMap(
    "path/to/root.ditamap",
    ditavalFilter=ditaval_filter,
    errors=errors,
    debug=False,
)

# 4. Build the key space manager from the resolved map
ksm = KeyspaceManager(resolvedMap=resolved_map, errors=errors)

# 5. Assemble DitaContext
ctx = DitaContext(
    keySpaceManager=ksm,
    ditavalFilter=ditaval_filter,
    errors=errors,
)
```

---

## DitaContext constructor parameters

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `keySpaceManager` | `KeyspaceManager` | required | Must be pre-populated |
| `keySpace` | `KeySpace` | `None` | Defaults to `ksm.getRootKeyspace()` |
| `mapContext` | `Element` | `None` | Current `<topicref>` or map element |
| `ditavalFilter` | `DitavalFilter` | `None` | Defaults to a pass-through filter |
| `errors` | `dict` | `{}` | **Always pass the same dict you used in steps 2–4** |
| `debug` | `bool` | `False` | Enables verbose print output |

---

## Common mistakes

### Wrong order: KeyspaceManager built before resolveMap
```python
# WRONG — KeyspaceManager receives an unresolved ElementTree
ksm = KeyspaceManager(resolvedMap=etree.parse("root.ditamap"))
```
`KeyspaceManager` expects a map that has already had submaps inlined by `resolvemap.resolveMap()`. Building it from a raw parse result silently produces an incomplete key space.

### Separate errors dicts
```python
# WRONG — errors reported during resolveMap() are not visible in DitaContext
resolved_map = resolvemap.resolveMap("root.ditamap", errors={})
ctx = DitaContext(ksm, errors={})
```
Use one `errors = {}` dict and pass it to every pydita call.

### Missing DITA-OT
`resolveMap()` calls `xmlutils.getDTDAwareParser()` which requires DITA-OT. If `DITA_OT_DIR` is not set:
```
KeyError: 'DITA_OT_DIR'
```
Set the environment variable or add `dita.ot.dir=/path/to/dita-ot` to `~/.build.properties`.

---

## Updating the context during processing

```python
# Switch the active key space (e.g., when entering a keyscoped submap)
ctx._keySpace = ctx.getKeyspaceManager().getKeyspaceByMapUri(submap_uri)

# Replace the DITAVAL filter
ctx.setDitavalFilter(new_filter)

# Record an error from within processing code
ctx.recordError("my-key", exception, operation="myFunction()")

# Enable debug logging
ctx.setDebug(True)
```

---

## Checking for errors after processing

```python
from pydita import loggingutils

if ctx.getErrors():
    print(loggingutils.reportErrors(ctx.getErrors(), showTraceBack=True))
```

---

## See also

- `map-resolve` — detailed `resolveMap()` API reference
- `keyspace-debug` — how to inspect and debug key spaces
- `error-handling` — full error model reference
