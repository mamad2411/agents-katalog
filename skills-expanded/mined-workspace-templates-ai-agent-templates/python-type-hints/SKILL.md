---
name: python-type-hints
description: Adds and tightens Python type hints, then runs mypy or pyright until clean without blanket ignores. Use it on untyped or loosely typed modules.
---

# Python type hints

Types are documentation the machine checks. Make them accurate before making them green.

## Steps

1. Detect the checker: look for `mypy.ini`, `[tool.mypy]` or `[tool.pyright]` in `pyproject.toml`, or `pyrightconfig.json`. Run it first and record the baseline error count.
2. Work one module at a time, starting with the leaves that others import.
3. Annotate every public function: parameters, return type, and `-> None` where it returns nothing. Prefer `list[str]` and `X | None` over `typing.List` and `Optional` on Python 3.10+.
4. Replace loose dicts with `TypedDict`, `dataclass` or `NamedTuple` when the keys are fixed. Use `Protocol` for duck-typed arguments and `TypeVar` or `ParamSpec` for decorators.
5. Prefer `Sequence` and `Mapping` for read-only parameters, concrete types for returns.
6. Run the checker after each module and fix errors by correcting the code or the type.

## Rules

- Never add `# type: ignore` without an error code and a one-line reason, for example `# type: ignore[arg-type]  # lib stubs wrong`.
- Do not use `Any` to silence an error. Use `object`, a union or a generic first.
- Never change runtime behavior to satisfy the checker unless it exposes a real bug, and say so when it does.
- Use `cast` sparingly and only after an `isinstance` check you can point to.

## Report

Baseline vs final error count, modules annotated, each remaining ignore with its reason, and real bugs the checker revealed.
