---
name: map-resolve
description: Reference skill for pydita's resolvemap module. Use this skill when you need to flatten a DITA map tree into a single in-memory document using resolveMap(), understand how submaps are inlined as topicgroup elements, apply DITAVAL filtering during resolution, or discover all files referenced by a map with getDirectFilesFromMap().
compatibility: Python 3.10+. Requires pydita (lxml). DTD-aware parsing requires a DITA Open Toolkit installation.
---

## Overview

`pydita.resolvemap` flattens a tree of DITA maps (root map + submaps) into a single `ElementTree`. This is equivalent to what the XSLT `resolve-map.xsl` library does in DITA-OT. The resolved map is the required input for `KeyspaceManager`.

---

## `resolveMap()` — API reference

```python
from pydita import resolvemap

resolved: ElementTree = resolvemap.resolveMap(
    rootmap,           # str path, IOBase file, or ElementTree
    ditavalFilter,     # DitavalFilter — default: pass-through (include everything)
    errors,            # dict — collects errors keyed by file path
    debug,             # bool — default False
)
```

### `rootmap` input forms

| Form | Example |
|------|---------|
| File path string | `"docs/root.ditamap"` |
| Open file object | `open("docs/root.ditamap")` |
| Parsed `ElementTree` | result of `etree.parse(...)` |

Any other type raises `Exception("Value … is not a recognized type")`.

### Return value

An `ElementTree` whose root element mirrors the root map element, with all local-scope `format="ditamap"` references replaced inline by a `<topicgroup base="submap">` wrapper containing the submap's children.

---

## How submaps are inlined

Each local submap reference (`<topicref format="ditamap" scope="local" href="sub.ditamap"/>`) becomes:

```xml
<topicgroup class="+ map/topicref mapgroup-d/topicgroup " base="submap"
            orig-href="sub.ditamap" orig-class="- map/topicref ">
  <topicmeta class="- map/topicmeta ">
    <navtitle class="- topic/navtitle ">Submap Title</navtitle>
  </topicmeta>
  <!-- submap's topicrefs and reltables copied here -->
</topicgroup>
```

Key attributes on the `topicgroup`:
- `base="submap"` — marker used by `ditautils` to detect inlined submaps
- `orig-href` — original href to the submap file
- `xml:base` — set to the submap's absolute URI so relative `href` values resolve correctly

---

## DITAVAL filtering during resolution

Elements excluded by the filter are **not copied** into the resolved map. This means excluded submaps are not resolved at all.

```python
from pydita.ditaval import DitavalFilter

# Build a filter from a .ditaval file
filter = DitavalFilter(ditavalFiles=["filters/internal.ditaval"], errors=errors)

resolved = resolvemap.resolveMap("root.ditamap", ditavalFilter=filter, errors=errors)
```

If no filter is provided, a pass-through `DitavalFilter()` (includes everything) is used automatically.

---

## `getDirectFilesFromMap()` — discover referenced files

```python
from pydita import ditautils

result = ditautils.getDirectFilesFromMap(resolved_map, errors=errors)
# result = {
#   "topics":   {"/abs/path/to/topic.dita", ...},
#   "maps":     {"/abs/path/to/root.ditamap", "/abs/path/to/sub.ditamap", ...},
#   "nondita":  {"/abs/path/to/image.png", ...},
# }
```

All paths are **absolute**. The root map itself is included in `"maps"`.

---

## Error handling

Parsing errors are recorded in the `errors` dict and re-raised as `ParseError` for submap failures. Always check `errors` after `resolveMap()`:

```python
errors = {}
resolved = resolvemap.resolveMap("root.ditamap", errors=errors)
if errors:
    from pydita import loggingutils
    print(loggingutils.reportErrors(errors))
```

Known limitation: the `# FIXME` in `resolveMap()` means root-map `ParseError` is recorded but not re-raised. A `None` resolved map after the call indicates a root-map parse failure.

---

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `KeyError: 'DITA_OT_DIR'` | DITA-OT not found by `getDTDAwareParser()` | Set `DITA_OT_DIR` env var or add to `~/.build.properties` |
| `ParseError` on submap | Submap XML is malformed or not found | Check `orig-href` paths are relative to the parent map |
| Resolved map missing content | Submap excluded by DITAVAL filter | Check filter conditions match submap's conditional attributes |
| Keys not found after resolution | Submap was not resolved (peer/external scope) | Only `scope="local"` submaps are inlined |

---

## See also

- `context-setup` — how to pass the resolved map into `KeyspaceManager` and `DitaContext`
- `keyspace-debug` — inspect the key spaces built from the resolved map
