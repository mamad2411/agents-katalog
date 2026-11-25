---
name: python-patterns
description: Python stack conventions agentic-forge applies when the detected stack is Python — the toolchain (pytest / ruff / mypy), idioms, testing discipline, layout, and the high-value Python pitfalls. Loaded on demand by develop / code-review and the software-engineer / qa-engineer roles after stack detection; kept off the always-on listing.
disable-model-invocation: true
---

# Python patterns

The Python stack pack: loaded by the `software-engineer` / `qa-engineer` roles (and the
`code-review` lint aspect) when `stacks.detect` reports Python. It carries only what is
**Python-specific** on top of [`engineering-standards`](../engineering-standards/SKILL.md) —
Claude already knows general Python; this encodes the conventions and gates agentic-forge
holds Python work to. (Mechanism: ADR 0015, by-stack detection + reference packs.)

## Toolchain

**Prefer the repo's own commands** — read `pyproject.toml` (`[tool.pytest]`, `[tool.ruff]`,
`[tool.mypy]`), `Makefile`/`tox.ini`/`noxfile.py`, and the CI workflow, and run *those*. The
`stacks.py` registry defaults are the fallback when the repo declares nothing:

| Job | Conventional command | Gate |
| --- | --- | --- |
| test | `pytest` (or `pytest -q`) | green; new behaviour covered |
| lint | `ruff check .` | clean (no new `# noqa`) |
| format | `ruff format .` | applied |
| types | `mypy .` | clean (no new `# type: ignore`) |

Run the type and lint checks on the changed files before declaring done; never silence a
checker to pass — fix the cause or justify the suppression in the diff.

## Idioms

- **Type everything** on public functions; keep `mypy` clean. Start modules with
  `from __future__ import annotations` so annotations stay cheap and forward-referenceable.
- Prefer **`dataclasses`** for records, **`pathlib.Path`** over `os.path` string-joining,
  **f-strings** for formatting, comprehensions / `enumerate` / `zip` over manual index loops.
- **EAFP** (`try/except`) over LBYL when racing the filesystem/dict; use **context managers**
  (`with`) for every resource (files, locks, connections).
- Keep the public surface explicit (`__all__`); avoid import-time side effects.

## Testing

- `pytest`, arrange–act–assert. Cover the **happy path plus a boundary and an error case** for
  each behaviour — not just the line.
- **`@pytest.mark.parametrize`** for case tables; **fixtures** for setup; **`tmp_path`** for
  filesystem work (never write into the repo or CWD).
- Tests must be **deterministic**: no real network, no wall-clock/`random` dependence — inject
  or freeze them. Assert on behaviour and error *type/message*, not incidental formatting.
- Never weaken, skip, or delete an existing test to go green.

## Pitfalls (Python-specific, high-value)

- **Mutable default arguments** (`def f(x=[])`) — use `None` + assign inside.
- **Bare `except:` / silent `except Exception`** — catch the narrowest type; re-raise with
  context (`raise X from e`) or handle deliberately. Never swallow.
- **Late-binding closures** in loops (capture the loop var via a default arg).
- **`==` vs `is`** — `is` only for `None`/singletons; mutable **class attributes** shared across
  instances; modifying a list **while iterating** it.
- **Secrets in logs / f-strings**; **floating-point `==`** (use `math.isclose`); blocking calls
  in async code.

## Definition of done (Python)

`ruff check` + `ruff format` clean, `mypy` clean (no new ignores), `pytest` green with the new
boundary/error tests, public surface typed, no existing test weakened — using the repo's own
commands where it declares them.
