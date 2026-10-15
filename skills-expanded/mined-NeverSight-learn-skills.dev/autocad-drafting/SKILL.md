---
name: autocad-drafting
description: >
  AutoCAD drafting via the autocad-mcp MCP server (8 tools: drawing, entity, layer,
  block, annotation, pid, view, system). Use when creating or modifying AutoCAD drawings,
  site plans, P&ID diagrams, equipment layouts, or any CAD automation through the
  autocad-mcp tools. Covers both File IPC (live AutoCAD LT) and ezdxf (headless DXF)
  backends. Essential for avoiding common pitfalls: parallel tool call races, LISP
  timeouts, dialog traps, and batch sizing. Use this skill whenever autocad-mcp tools
  are invoked.
---

# AutoCAD Drafting via autocad-mcp

## Critical Rules

**NEVER call multiple autocad-mcp tools in parallel.** The File IPC backend is
single-threaded. Concurrent calls race at the IPC level and corrupt the dispatch,
triggering APPLOAD dialogs and timeouts. Always call tools sequentially.

**Prefer `execute_lisp` for bulk operations.** A single `execute_lisp` call with 5-7
`(command ...)` invocations is faster and more reliable than 5-7 separate tool calls
(each incurs ~1-2s IPC round-trip overhead).

**Keep `execute_lisp` batches under ~500 lines / 7 commands.** Exceeding the IPC timeout
(default 10s, configurable via `AUTOCAD_MCP_IPC_TIMEOUT`) leaves AutoCAD stuck in a
pending command state. Smaller batches are safer.

## Drawing Workflow

Follow this sequence for any drawing task:

1. **Verify connection** - `system(operation="status")` to confirm backend
2. **Set up layers** - Create all layers before any geometry
3. **Create geometry** - Equipment outlines, site boundaries, piping
4. **Add annotations** - Equipment tags, text labels, notes
5. **Add dimensions** - Linear, aligned, angular
6. **Title block** - Border, title text, project info
7. **Screenshot QA** - `view(operation="get_screenshot")` to verify, iterate

## `execute_lisp` Patterns

Use `system(operation="execute_lisp", data={"code": "..."})` for bulk work.

**Layer setup batch:**
```lisp
(progn
  (if (not (tblsearch "LAYER" "EQUIPMENT"))
    (command "_.-LAYER" "_NEW" "EQUIPMENT" "_COLOR" "cyan" "EQUIPMENT" ""))
  (if (not (tblsearch "LAYER" "PIPING"))
    (command "_.-LAYER" "_NEW" "PIPING" "_COLOR" "blue" "PIPING" ""))
  "layers created"
)
```

**Equipment placement batch (5-7 items max):**
```lisp
(progn
  (setvar "CLAYER" "EQUIPMENT")
  (command "_RECTANG" (list 5 20 0) (list 15 30 0))
  (command "_CIRCLE" (list 40 25 0) 8)
  (command "_RECTANG" (list 55 18 0) (list 70 32 0))
  "equipment placed"
)
```

**Text annotations — use `entmake`, NOT `(command "_TEXT" ...)`:**

`(command "_TEXT" "J" "ML" ...)` has unreliable prompt sequences that leave AutoCAD in an
input-waiting state, blocking subsequent dispatches. Always use `entmake` for text:

```lisp
(progn
  (setvar "CLAYER" "ANNOTATION")
  ;; Helper: tag + description at (x, y) with height ht
  (defun make-tag (x y tag desc ht / )
    (entmake (list '(0 . "TEXT") (cons 10 (list x y 0)) (cons 40 ht) (cons 1 tag)
      (cons 72 1) (cons 11 (list x y 0)) '(8 . "ANNOTATION")))
    (entmake (list '(0 . "TEXT") (cons 10 (list x (- y (* ht 1.3)) 0))
      (cons 40 (* ht 0.7)) (cons 1 desc) (cons 72 1)
      (cons 11 (list x (- y (* ht 1.3)) 0)) '(8 . "ANNOTATION")))
  )
  (make-tag 10 25 "P-101" "PUMP STATION" 1.5)
  (make-tag 40 25 "CL-201" "CLARIFIER" 1.5)
  "annotations placed"
)
```

**Flow arrows — use `entmake` LWPOLYLINE, NOT `(command "_SOLID" ...)`:**

`_SOLID` has the same prompt-sequence problem as `_TEXT`. Use closed LWPOLYLINE:

```lisp
(progn
  (setvar "CLAYER" "PIPING")
  ;; Helper: arrow at (x,y) pointing in direction "R"/"L"/"D"/"U"
  (defun make-arrow (x y dir / p1 p2 p3)
    (cond
      ((= dir "R") (setq p1 (list x (+ y 0.5)) p2 (list (+ x 2) y) p3 (list x (- y 0.5))))
      ((= dir "D") (setq p1 (list (- x 0.5) y) p2 (list x (- y 2)) p3 (list (+ x 0.5) y)))
      ((= dir "L") (setq p1 (list x (- y 0.5)) p2 (list (- x 2) y) p3 (list x (+ y 0.5))))
      ((= dir "U") (setq p1 (list (+ x 0.5) y) p2 (list x (+ y 2)) p3 (list (- x 0.5) y)))
    )
    (entmake (list '(0 . "LWPOLYLINE") '(100 . "AcDbEntity") '(8 . "PIPING")
      '(100 . "AcDbPolyline") '(90 . 3) '(70 . 1)
      (cons 10 p1) (cons 10 p2) (cons 10 p3)))
  )
  (make-arrow 16 25 "R")
  "arrow placed"
)
```

## Tool Selection Guide

| Task | Tool | Notes |
|------|------|-------|
| Single entity | `entity(operation="create_*")` | Use for one-off entities |
| Bulk entities (3+) | `system(operation="execute_lisp")` | Batch in `(progn ...)` |
| Layer operations | `layer(operation="*")` or `execute_lisp` | Either works; batch if 3+ |
| Dimensions | `annotation(operation="create_dimension_*")` | One at a time is fine |
| Screenshot | `view(operation="get_screenshot")` | Returns PNG image |
| Undo mistake | `drawing(operation="undo")` | Single undo step |
| Save | `drawing(operation="save")` | Add `data: {path}` for save-as |
| Open file | `drawing(operation="open", data={"path": "..."})` | DWG or DXF |
| P&ID symbols | `pid(operation="insert_*")` | Requires CTO library |

## Reload Dispatcher Without Human Intervention

If mcp_dispatch.lsp needs reloading after an update:

```
system(operation="execute_lisp", data={"code":
  "(progn (setvar \"SECURELOAD\" 0) (load \"C:/Users/hvksh/mcp-servers/autocad-mcp/lisp-code/mcp_dispatch.lsp\") (setvar \"SECURELOAD\" 1) \"dispatch reloaded\")"
})
```

## Pitfalls and Mitigations

| Pitfall | Cause | Mitigation |
|---------|-------|------------|
| APPLOAD dialog | Parallel tool calls interleave PostMessageW keystrokes | Never call tools in parallel |
| IPC timeout | Batch too large or command awaiting input | Keep batches under 7 commands |
| Stuck command | Previous timeout left AutoCAD in command prompt | Server sends ESC prefix automatically (v3.1+) |
| SECURELOAD dialog | `(load)` on untrusted path | Server suppresses automatically (v3.1+) |
| `drawing.create` resets | Erases all + purges current drawing (not `_.NEW`) | LISP namespace preserved; no new tab |
| Non-ASCII crash | LISP writes cp1252, Python reads UTF-8 | Server falls back to cp1252 (v3.1+) |
| `drawing.save` ignores path | Old LISP did QSAVE always | Fixed in v3.1 — uses SAVEAS when path given |
| TEXT/SOLID timeout | `(command "_TEXT" "J" "ML" ...)` and `_SOLID` have unreliable prompt sequences | Use `entmake` instead — no command-line interaction |

## Backend Differences

| Feature | File IPC (live AutoCAD) | ezdxf (headless) |
|---------|------------------------|-------------------|
| `execute_lisp` | Yes | Not supported |
| `undo` / `redo` | Yes | Not supported |
| `plot_pdf` | Yes | Not supported |
| `offset` / `fillet` / `chamfer` | Yes | Not supported |
| Screenshot | Win32 PrintWindow | matplotlib render |
| Platform | Windows only | Any (Linux/Mac/WSL) |

## Reference

For detailed tool operations, see [tool-reference.md](references/tool-reference.md).
