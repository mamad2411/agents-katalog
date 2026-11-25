---
description: "Nexi's safety gates — Forge code scanning and tool approval-token stripping. Use before touching engine/forge/safety_scan.py, engine/tool_registry.py execute_tool, or engine/approval_queue.py."
license: "MIT"
---
# Nexi Safety Gate

Two independent gates. Both are defense-in-depth, not proof of safety — treat
either as a hard boundary to preserve, not relax, when debugging.

## 1. Forge code-generation gate — `engine/forge/safety_scan.py`

`scan(code)` AST-walks generated tool code BEFORE it ever executes (even in
the sandbox). `safe: True` only means "no obvious system access" — it does
not mean the code is harmless.

- `SAFE_MODULES` allowlists pure-compute stdlib (math/json/re/...). Any other
  import is flagged.
- `DANGEROUS_CALLS` blocks `eval/exec/compile/open/__import__/input/
  breakpoint` plus the reflection primitives `getattr/setattr/delattr/vars/
  globals/locals/memoryview` — these are the standard ways to bypass an AST
  allowlist (e.g. `getattr(__builtins__, '__import__')`).
- `_is_dunder(name)` flags ANY dunder attribute/name reference
  (`__class__`, `__subclasses__`, `__mro__`, `__globals__`,
  `__builtins__`, ...) — pure-compute code has no legitimate reason to touch
  one, so this is a single rule that closes the whole sandbox-escape family.
  Do not narrow this to a specific dunder list; that's how it got bypassed
  before.
- `forge_engine` must gate on this result BEFORE executing generated code,
  never after.

## 2. Tool-execution approval gate — `engine/tool_registry.py` + `engine/approval_queue.py`

`execute_tool()` strips any model-supplied `_approval_token` /
`_studio_auth` / `approval_token` / `authorization` / `confirmed` slot before
anything reads it (`react_planner._strip_reserved_arguments`, or a manual
pop-list fallback).

- The ONLY legitimate approval path is `approval_queue.approve()`, which
  re-invokes `execute_tool` with a private, unguessable sentinel under
  `_APPROVAL_TOKEN_KEY == _INTERNAL_APPROVAL` (imported from
  `engine.approval_queue`). That exact value is captured BEFORE stripping so
  a real approval still proceeds.
- Real user confirmation is granted only via the explicit `confirmed=` kwarg
  that Nexi itself sets — never by a slot the model wrote into its own tool
  call. A model claiming `"confirmed": true` in its arguments must have that
  claim stripped, not honored.
- When adding a new gated tool (`safety="high"` in `_TOOLS`), route its
  approval through `approval_queue`, don't invent a new confirmation flag.

## Debugging checklist

- Gate rejecting code that looks safe? Check which specific flag fired
  (`scan()["flags"]`) before loosening a rule — the flag is almost always
  correct that the pattern is a bypass primitive.
- Tool executing without approval? Check `execute_tool` is actually calling
  `_strip_reserved_arguments` on the path you're debugging (there are two
  dispatch paths: ReAct and direct `command.py`) — both must strip.
