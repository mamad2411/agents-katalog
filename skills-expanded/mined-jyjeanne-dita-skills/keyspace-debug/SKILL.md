---
name: keyspace-debug
description: Guides debugging of pydita key space construction and key resolution failures. Use this skill when keys are not resolving, keyscoped references return None, duplicate key warnings appear, or you need to inspect the key space tree structure built by KeyspaceManager from a resolved DITA map.
compatibility: Python 3.10+. Requires pydita (lxml, anytree). Must have a valid resolved map from resolvemap.resolveMap() before building the key space.
---

## Overview

pydita implements the DITA 1.3 key space algorithm in `pydita.keyspace` and `pydita.keyspacemgr`. A key space is a tree of `KeySpace` nodes, each containing `KeyDefinition` children — one per key name. The root key space is built from the resolved map; child key spaces are created for every `@keyscope` boundary.

---

## Key classes

| Class | Module | Role |
|-------|--------|------|
| `KeyspaceManager` | `keyspacemgr` | Top-level manager; builds and indexes all key spaces |
| `KeySpace` | `keyspace` | One key space (one `@keyscope` scope); contains `KeyDefinition` children |
| `KeyDefinition` | `keyspace` | One key name → one or more key-defining elements (priority order) |

---

## Inspecting the key space tree

### Print the full tree

```python
from anytree import RenderTree
from pydita.keyspacemgr import KeyspaceManager

ksm = KeyspaceManager(resolvedMap=resolved_map, errors=errors)
root_ks = ksm.getRootKeyspace()

for pre, _, node in RenderTree(root_ks):
    print(f"{pre}{node.label}")
```

Output example:
```
KeySpace: #annonymous
├── KeyDef: product-name
├── KeyDef: version
└── KeySpace: enterprise-scope
    ├── KeyDef: product-name   ← overrides parent
    └── KeyDef: ent-feature
```

### Use the built-in text reporter

```python
from pydita.keyspacevisitors import KeyspaceReportingVisitor

reporter = KeyspaceReportingVisitor()
print(reporter.reportKeySpace(ksm.getRootKeyspace()))
```

---

## Looking up keys

### Context-free lookup (root key space)

```python
root_ks = ksm.getRootKeyspace()
key_def = root_ks.resolveKey("product-name")

if key_def is None:
    print("Key not defined in root scope")
else:
    # getKeyDefiners() returns key-defining elements in priority order
    first_elem = key_def.getKeyDefiners()[0]
    href = first_elem.get("href")
    print(f"Key 'product-name' -> href={href}")
```

### Keyscoped lookup

```python
# Get child key spaces by scope name (returns a list — scope names need not be unique)
scoped_spaces = ksm.getRootKeyspace().getKeyspacesByScopeName("enterprise-scope")
if scoped_spaces:
    key_def = scoped_spaces[0].resolveKey("product-name")
```

### Lookup by map URI

```python
ks = ksm.getKeyspaceByMapUri("/abs/path/to/submap.ditamap")
```

---

## Common problems and how to diagnose them

### Key resolves to `None`

1. Check the key name is spelled correctly (case-sensitive).
2. Verify the `<keydef>` element exists in the resolved map:
   ```python
   keydefs = resolved_map.xpath("//*[@keys]")
   for kd in keydefs:
       print(kd.get("keys"), kd.get("href"))
   ```
3. Check the `<keydef>` was not excluded by the DITAVAL filter (it won't appear in the resolved map if filtered out).
4. If the key is in a submap with `@keyscope`, you must look it up in the child key space, not the root.

### Key space not built for a submap

Submaps become child key spaces only when they carry a `@keyscope` attribute. A submap without `@keyscope` contributes its key definitions directly to the parent scope.

```python
# Check which key spaces exist
for ks_uri, ks in ksm.keyspacesByMapUri.items():
    print(ks_uri, "->", ks.label)
```

### Duplicate key warning

The first definition wins (DITA 1.3 §2.4.4.2). Subsequent definitions are stored in `key_def.keydefElems` at lower priority indexes. Use the reporter to see all definitions:

```python
reporter = KeyspaceReportingVisitor()
print(reporter.reportKeySpace(ksm.getRootKeyspace()))
```

### Recursive key definition

If a `<keydef>` uses `@keyref` that eventually points back to itself, pydita will detect it and record an error. Check `errors` for entries containing `"recursive"`.

---

## Key space construction algorithm

The construction runs in two phases after `resolveMap()`:

1. **Pull-up** (`PullUpVisitor`): walks the resolved map and creates `KeyDefinition` nodes. Keys defined in a keyscoped submap are placed in a child `KeySpace`.
2. **Push-down** (`PushDownVisitor`): propagates parent-scope key definitions down to child scopes so child scopes can fall back to parent definitions.

If you suspect a bug in construction, enable debug:
```python
ksm = KeyspaceManager(resolvedMap=resolved_map, errors=errors, debug=True)
```

---

## See also

- `context-setup` — full pipeline setup including KeyspaceManager initialisation
- `map-resolve` — ensure the resolved map is correct before building key spaces
