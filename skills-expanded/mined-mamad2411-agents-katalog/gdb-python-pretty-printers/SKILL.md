---
name: gdb-python-pretty-printers
description: >
  Write and load GDB Python pretty-printers for custom C/C++ types: gdb.printing
  API, lookup functions, children/to_string, auto-load from objfiles, and debugging
  printer failures. Use for local/lab binaries and authorized reverse-engineering —
  not to bypass protections on third-party systems without authorization.
---

# GDB Python Pretty-Printers

## Scope And Authorization

- **In scope:** Binaries you own, labs, CTFs, authorized RE engagements.
- **Out of scope:** Attaching to third-party production processes without authorization.
- Pretty-printers execute **Python inside GDB** with access to inferior memory — treat
  printer code as trusted; do not load untrusted printer scripts blindly.
- Pair deep RE workflows with binary-re skills; this skill focuses on printer authoring.

## When To Use

- `print` of structs/containers is unreadable (libstdc++, custom ropes, tagged unions).
- Shipping SDK libraries with `*-gdb.py` auto-load helpers.
- Speeding up debugging of domain types (packets, arena blocks, smart handles).
- Teaching juniors how GDB Python printers resolve types.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General Ghidra static analysis | `ghidra-headless-analyze` / scripting skills |
| GDB core dump triage only | broader gdb RE skills |
| RR / time-travel debugging | specialized debugger skills |
| Production observability | `observability-metrics-tracing` |
| Implementation quality of product code | `code-quality-standards` |

## Concepts

| Piece | Role |
| --- | --- |
| `gdb.Value` | Inferior object view |
| Pretty-printer object | Implements `to_string`, optional `children`, `display_hint` |
| Lookup function | Maps type name / tag → printer instance |
| `gdb.printing.RegexpCollectionPrettyPrinter` | Regex register helper |
| Auto-load | `objfile`-relative `*-gdb.py` when safe-path allows |
| `set print pretty on` | Formatting; printers still do semantic decode |

### Printer interface (minimum)

```python
class MyTypePrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        return "MyType(...)"

    def children(self):
        # yield (name, gdb.Value_or_python)
        yield ("field", self.val["field"])

    def display_hint(self):
        return "map"  # or "array", "string", None
```

## Workflow

### 1. Confirm binary and types

1. Build with debug symbols (`-g`); note C++ ABI / libstdc++ version if relevant.
2. Identify types that need printers (`ptype`, header definitions).
3. Success: `print var` shows domain meaning without manual field walks.

```bash
gdb --version
gdb ./app
# (gdb) info auto-load
# (gdb) show auto-load safe-path
```

### 2. Baseline without printer

```gdb
(gdb) file ./app
(gdb) start
(gdb) ptype MyType
(gdb) print my_var
(gdb) print /x my_var
```

Capture raw layout for regression comparison.

### 3. Author printer module

```python
# mytype_printers.py
import gdb
import gdb.printing

class MyTypePrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        kind = int(self.val["kind"])
        return f"MyType(kind={kind})"

    def children(self):
        yield ("kind", self.val["kind"])
        yield ("payload", self.val["payload"])

def build_pretty_printer():
    pp = gdb.printing.RegexpCollectionPrettyPrinter("myproject")
    pp.add_printer("MyType", "^MyType$", MyTypePrinter)
    # C++ may need: ^MyNamespace::MyType$
    return pp

def register(objfile=None):
    gdb.printing.register_pretty_printer(
        objfile, build_pretty_printer(), replace=True
    )

if __name__ == "__main__":
    register()
```

Notes:

- Match **canonical** type names as GDB sees them (`whatis`, `ptype`).
- C++ templates: regex carefully; consider `gdb.types.get_basic_type`.
- Never infinite-recurse: do not `print` same value inside `to_string` via Python API
  without guards.

### 4. Load printers

**Manual:**

```gdb
(gdb) source /path/to/mytype_printers.py
(gdb) python register()
(gdb) print my_var
```

**Auto-load** (objfile-relative): place `app-gdb.py` next to binary per GDB docs; ensure:

```gdb
(gdb) add-auto-load-safe-path /path/to/project
```

### 5. Debug printer failures

| Symptom | Check |
| --- | --- |
| Printer not applied | Regex vs `whatis`; register on correct objfile |
| Python exception on print | `set python print-stack full` |
| Wrong fields | Padding / optimized-out; use `val.type.fields()` |
| Slow printing | Avoid walking huge containers without limits |
| Auto-load blocked | safe-path / `with-auto-load` settings |

```gdb
(gdb) set python print-stack full
(gdb) info pretty-printer
(gdb) disable pretty-printer global myproject; print my_var
(gdb) enable pretty-printer global myproject
```

### 6. Test suite for printers

1. Small C/C++ fixture binary with known values.
2. GDB batch script:

```bash
gdb -batch -nx \
  -ex "source mytype_printers.py" \
  -ex "python register()" \
  -ex "file ./fixture" \
  -ex "run" \
  -ex "print sample" \
  -ex "quit"
```

3. Assert stdout contains expected rendering.
4. CI optional on linux runners with gdb package.

### 7. Hand off

- Document load instructions in `CONTRIBUTING` / `docs/debugging.md`.
- Version printers with library ABI changes.
- For libstdc++/LLVM, prefer system printers; only override project types.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Matching | Regex on full type name tests | Guess short names only |
| Safety | Trusted scripts + safe-path | `source` random gist as root |
| Output | Small to_string + children | Dump 10MB vector inline |
| C++ | Handle references/typedefs | Crash on optimized-out |
| Maintenance | Fixture tests in CI | Printer bitrots silently |

## Output Checklist

- [ ] Binary/symbols/authorization recorded
- [ ] Target types listed with sample `ptype`
- [ ] Printer module implements to_string/children as needed
- [ ] Registered and verified in interactive GDB
- [ ] Auto-load path documented (if used)
- [ ] Failure debugging notes (stack full) captured once
- [ ] Batch fixture test optional but preferred
- [ ] No untrusted code in auto-load paths
- [ ] Docs updated for developers

## Rules

- Authorized debugging only.
- Treat GDB Python as code execution in the debugger context.
- Prefer official `gdb.printing` registration APIs.
- Keep printers pure display — no mutation of inferior unless explicitly debugging.
- Focus on pretty-printers; broader RE techniques live elsewhere.
