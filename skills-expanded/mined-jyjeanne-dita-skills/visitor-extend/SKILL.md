---
name: visitor-extend
description: Guides implementation of custom Visitor and Visitable classes in pydita. Use this skill when you need to write a new tree walker for KeySpace or KeyDefinition nodes, implement a custom report generator, or understand how the existing visitors (PullUpVisitor, PushDownVisitor, KeyspaceReportingVisitor, DitavalVisitor) work so you can extend or replace them.
compatibility: Python 3.10+. Requires pydita (anytree for key space tree nodes).
---

## Overview

pydita uses the **Visitor** design pattern throughout. Base classes are in `pydita.visitor`. The base `Visitor.visit()` is a **no-op** — dispatch is handled by each domain-specific subclass using `isinstance` checks:

- **Key space visitors** (`pydita.keyspacevisitors`): extend `KeyspaceVisitor` and override `visitKeySpace(keySpace)` and/or `visitKeyDefinition(keyDef)` (camelCase).
- **DITAVAL visitors** (`pydita.ditavalvisitors`): extend `DitavalVisitor` and override `visit_DitavalFilter(filter)` and/or `visit_DitavalCondition(condition)`.
- **Generic visitors**: override `visit(obj)` directly and use `isinstance` checks.

Key space nodes (`KeySpace`, `KeyDefinition`) and DITAVAL nodes (`DitavalCondition`) all implement `Visitable`.

---

## Base classes

### `Visitable`

```python
from pydita.visitor import Visitable

class Visitable:
    def accept(self, visitor: 'Visitor') -> None:
        """Calls visitor.visit(self)."""
        visitor.visit(self)
```

Any class that should be walkable must inherit from `Visitable` and call `accept()` on its children.

### `Visitor`

```python
from pydita.visitor import Visitor

class Visitor:
    def visit(self, node: Visitable) -> None:
        """No-op in the base class. Domain subclasses override this."""
        pass
```

`KeyspaceVisitor` overrides `visit()` to dispatch via `isinstance`:
- `isinstance(obj, KeySpace)` → calls `self.visitKeySpace(obj)`
- `isinstance(obj, KeyDefinition)` → calls `self.visitKeyDefinition(obj)`

---

## Writing a custom key space visitor

### Step 1 — Subclass `KeyspaceVisitor`

Override `visitKeySpace` and/or `visitKeyDefinition` (camelCase, no underscore):

```python
from pydita.keyspacevisitors import KeyspaceVisitor
from pydita.keyspace import KeySpace, KeyDefinition

class MyKeyspaceVisitor(KeyspaceVisitor):

    def __init__(self):
        super().__init__()
        self.report_lines: list[str] = []

    def visitKeySpace(self, node: KeySpace) -> None:
        self.report_lines.append(f"KeySpace: {', '.join(node.getScopeNames())}")
        # Walk key definitions in this space
        for kd in node.getKeyDefinitions():
            self.visit(kd)          # dispatches to visitKeyDefinition
        # Recurse into child key spaces
        for child in node.getChildSpaces():
            self.visit(child)       # dispatches to visitKeySpace

    def visitKeyDefinition(self, node: KeyDefinition) -> None:
        hrefs = [e.get("href", "(no href)") for e in node.getKeyDefiners()]
        self.report_lines.append(f"  Key '{node.getKeyName()}' -> {hrefs}")

    def get_report(self) -> str:
        return "\n".join(self.report_lines)
```

### Step 2 — Invoke it

```python
visitor = MyKeyspaceVisitor()
ksm.getRootKeyspace().accept(visitor)   # accept() calls visitor.visit(root_ks)
print(visitor.get_report())
```

---

## Making your own class Visitable

```python
from pydita.visitor import Visitor, Visitable

class MyDitaNode(Visitable):

    def __init__(self, name: str, children: list = None):
        self.name = name
        self._children = children or []

    def accept(self, visitor: Visitor) -> None:
        visitor.visit(self)           # dispatch to visit_MyDitaNode
        for child in self._children:  # walk children
            child.accept(visitor)
```

> **Important:** `Visitable.accept()` only dispatches to the visitor — it does **not** recurse into children automatically. You must call `child.accept(self)` inside your `visit_*` methods (or inside `accept()`) to walk the tree.

---

## Existing visitors — reference

### `PullUpVisitor` (`keyspacevisitors`)
Walks the resolved map (an `ElementTree`) and builds `KeyDefinition` entries inside `KeySpace` nodes. Called internally by `constructKeySpace()` in `keyspacemgr`.

### `PushDownVisitor` (`keyspacevisitors`)
Propagates parent key definitions down into child key scopes. Runs after `PullUpVisitor`.

### `KeyspaceReportingVisitor` (`keyspacevisitors`)
Produces a human-readable text report of a key space tree.

```python
from pydita.keyspacevisitors import KeyspaceReportingVisitor

reporter = KeyspaceReportingVisitor()
print(reporter.reportKeySpace(ksm.getRootKeyspace()))
```

### DITAVAL visitors (`ditavalvisitors`)
Generate an Excel report from a `DitavalFilter`. Use `DitavalFilter.accept(visitor)` to invoke.

---

## Visitor pattern pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `visitKeySpace` never called | Forgot to call `super().__init__()` in subclass | Always call `super().__init__(debug=debug)` |
| Tree walk stops after root | `visitKeySpace` doesn't recurse | Add `for child in node.getChildSpaces(): self.visit(child)` |
| Stack overflow | Circular parent-child relationship in `anytree` | Not possible with valid pydita trees; check for custom node wiring |
| Visitor misses `KeyDefinition` nodes | Only `visitKeySpace` defined | Add `visitKeyDefinition` method |
| Custom `visit_*` method never called | Using underscore-style methods on `KeyspaceVisitor` | Use `visitKeySpace` / `visitKeyDefinition` (camelCase, not snake_case) |

---

## Full example — collect all hrefs from a key space

```python
from pydita.keyspacevisitors import KeyspaceVisitor
from pydita.keyspace import KeySpace, KeyDefinition

class HrefCollector(KeyspaceVisitor):

    def __init__(self):
        super().__init__()
        self.hrefs: list[tuple[str, str]] = []  # (key_name, href)

    def visitKeySpace(self, ks: KeySpace) -> None:
        for kd in ks.getKeyDefinitions():
            self.visit(kd)                       # dispatches to visitKeyDefinition
        for child in ks.getChildSpaces():
            self.visit(child)                    # recurse into scoped children

    def visitKeyDefinition(self, kd: KeyDefinition) -> None:
        for elem in kd.getKeyDefiners():
            href = elem.get("href")
            if href:
                self.hrefs.append((kd.getKeyName(), href))

# Usage
collector = HrefCollector()
ksm.getRootKeyspace().accept(collector)
for key_name, href in collector.hrefs:
    print(f"{key_name}: {href}")
```

---

## See also

- `keyspace-debug` — inspect existing key spaces without writing a visitor
- `context-setup` — full pipeline setup that produces the `KeyspaceManager` to walk
