---
name: abacus-add-function
description: How to add (or remove/rename/alias) a built-in function in the abacus expression language — math functions like sqrt/sin/hypot/atan2, variadic stats like sum/median, nullary constants like pi/e/time. Use whenever the task is to implement a new abacus call function, add a function alias, make a function multi-argument, or wire a new constant. Covers the Value method + registry two-step, per-mode (fixed-point/floating-point/rational) conventions, arity, help text, tests, and the verification commands. For adding a whole new numeric TYPE/mode (not a function), see CONTRIBUTING.md instead.
---

# Adding a function to the abacus language

A function is a **two-step, local change**: implement a method on `Value`, then
register its name. The lexer, parser, and evaluator are all generic over the
registries — they never branch on a function name, so you never touch them.

Files (anchors drift; search by symbol, don't trust line numbers):
- `src/mcp_abacus/expr/value.py` — the `Value` class; per-mode math lives here.
- `src/mcp_abacus/expr/nodes.py` — the registries `_FUNCS`, `_NULLARY_FUNCS`,
  `CONSTANT_NAMES`, `FUNCTION_HELP`; arity (`FUNCTION_ARITIES`) is derived here.
- `tests/test_functions.py` — functional tests driving the real `calculate` tool.
- `tests/test_reference.py` — drift guards (no manual edit needed; must stay green).

## Step 1 — implement the method on `Value`

Add one method to the `Value` class in `value.py`. `self` IS the first operand.
The body is a `match self.mode:` with **one case per `Mode` member** plus a
`case _:` that raises `ValueError(f"unsupported mode: {self.mode!r}")`. Return a
**new** `Value` (immutable); never mutate `self`.

Pattern (see `Value.sqrt` for the canonical example):

```python
def hypot(self, other: "Value") -> "Value":
    """One-line-per-mode contract: what's exact, what's inexact, what's refused."""
    match self.mode:
        case Mode.FLOATING_POINT:
            assert isinstance(self.payload, float)
            ...
            return Value(Mode.FLOATING_POINT, result, exact=False)  # binary64 always inexact
        case Mode.FIXED_POINT:
            assert isinstance(self.payload, FixedPoint)
            ...  # work on scaled int mantissas; round half-to-even back to the scale
            return Value(Mode.FIXED_POINT, FixedPoint(mantissa, decimals), exact=exact)
        case Mode.RATIONAL:
            assert isinstance(self.payload, Fraction)
            ...  # exact-or-refuse: if the result is irrational, raise
            return Value(Mode.RATIONAL, result, exact=self.exact)
        case _:
            raise ValueError(f"unsupported mode: {self.mode!r}")
```

Conventions:
- **Name**: matches the registry key. Add a trailing underscore only to dodge a
  Python builtin/keyword (`abs_`, `sum_`, `min_`, `max_`); the registry maps the
  public name to it (`"abs": Value.abs_`).
- **Exactness**: propagate `self.exact` when the op stays on the type's grid; set
  `exact=False` on any rounding; binary64 (`FLOATING_POINT`) is unconditionally
  inexact. For binary ops, gate exactness on **both** operands — existing code
  uses `self._same_mode(other, "op")`, which also rejects mixed modes.
- **Domain errors**: raise `NotRepresentableError("lowercase reason")` for things
  the mode can't represent (negative `sqrt`, irrational rational result, sine of a
  non-zero rational). The node layer wraps it into a line-tagged `EvalError`.
- **`rational` is exact-or-refuse**: if a value is irrational there, refuse — do
  not approximate. `fixed-point` is the flagship mode (crypto/money); support it
  via scaled-integer arithmetic with guard digits and half-to-even rounding.
- **Arity is read off the signature** — declare it correctly:
  - unary `def f(self)` → `(1, 1)`
  - binary `def f(self, other)` → `(2, 2)`
  - variadic `def f(self, *others)` → `(1, None)` (declares a *minimum*)
  - optional trailing arg `def f(self, ndigits=None)` → `(1, 2)` (28.22): a
    positional param **with a default** is optional — it lifts the max, not the min.
    The absent arg is filled by the Python default at dispatch, so the body must
    handle `ndigits=None`. The `floor`/`ceil`/`round`/`trunc` family uses this shape.

## Step 2 — register the name in `nodes.py`

Add to `_FUNCS` (name → method) **and** `FUNCTION_HELP` (name → one-line facts,
no signature — the reference prepends it). Arity is derived automatically; the
parser and `functions` help section read the live registry, so nothing else needs
editing.

```python
# _FUNCS
"hypot": Value.hypot,  # short comment; cite the TODO item if there is one
# FUNCTION_HELP
"hypot": "euclidean distance sqrt(x^2+y^2); inexact except on the type's grid",
```

Invariant enforced by `test_reference.py`: `set(FUNCTION_HELP) == set(FUNCTION_ARITIES)`.
Every name — including aliases and nullaries — must have exactly one help entry.

Variants:
- **Alias**: a second `_FUNCS` key pointing at the same method (`"ln": Value.log`)
  plus its own `FUNCTION_HELP` line (e.g. `"natural log; alias of log"`).
- **Nullary** (zero args, e.g. a constant or clock read): put it in
  `_NULLARY_FUNCS` instead. Its method takes `EvalContext` (mode, scale, clock),
  not operands, and is dispatched with the context. Arity is forced to `(0, 0)`.
  Still needs a `FUNCTION_HELP` entry.
- **Bare constant** (usable without parens, like `pi`/`e`): also add the name to
  `CONSTANT_NAMES`. Every name there MUST be a key of `_NULLARY_FUNCS`. A reading
  action (like `time`) stays an explicit call — do not add it as a constant.

## Step 3 — tests

Add a `@pytest.mark.parametrize`-driven `test_<func>` to `tests/test_functions.py`,
following `test_abs` / `test_sqrt`. These drive the real `calculate` tool in-process
via the `_calc` / `_value` helpers and assert the annotated value string. Cover:
- **all three modes** (omit `mode` for the fixed-point default, plus
  `"floating-point"` and `"rational"`);
- edge cases: zero, negatives, scale preservation, exact vs inexact;
- domain refusals in their own test, asserting the line-tagged `error` string and
  `value is None` (see the `sqrt` refusal test).

Also update the **hardcoded arity mirror** in `tests/test_nodes.py`
(`test_function_arities_match_the_registry` asserts `FUNCTION_ARITIES == {...}`
literally) — add your function's `(min, max)` row, or that test fails. This is the
one registry whose test is NOT auto-derived.

To get the exact value strings for the `calculate`-driven tests without
hand-computing the rendered `(inexact, rounded …)` suffix, call the tool
in-process once and copy what it prints, then sanity-check the numbers against
Python's `math` before baking them in:

```python
import asyncio, json
from mcp_abacus.server import mcp
r = asyncio.run(mcp.call_tool("calculate", {"expression": "exp(2.000000)"}))
print(json.loads((r[0] if isinstance(r, tuple) else r)[0].text)["value"])
```

## Step 4 — docs & verify

- Update `README.md` if the function is user-facing (it lists supported functions).
- This project is **TODO-driven**: check off the relevant item in `TODO` rather
  than adding new ones, and do not add TODO entries without being asked. Keep
  commit/docstring as the source of truth, not the TODO.
- Run the checks (CI runs them on 3.10–3.13):

```bash
./run-tests.sh          # pytest with a per-failure summary (or: uv run pytest)
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

`test_reference.py` will fail loudly if you registered a function without help, or
left help for a function you removed — that's the guard that keeps the help, the
parser, and the implementations from drifting.
