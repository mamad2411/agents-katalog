# Django Imports

## Summary

**One-sentence:** Produces a Django import-discipline ruleset: alias cross-app imports (apps.users.models as users_models), never direct symbol imports; isort first-party config and a lint rule that fails on bare model imports.

**One-paragraph:** Produces a Django import-discipline ruleset: alias cross-app imports (apps.users.models as users_models), never direct symbol imports; isort first-party config and a lint rule that fails on bare model imports. The methodology fires on a named trigger, produces a fixed-shape artifact with evidence anchors and a named owner, and is reviewed against outcomes at a published cadence so it stops being folklore.

**Ефективно для:** команд, що оперують цим артефактом регулярно і потребують детермінованого формату плюс перевірюваного результату.

## Applies If (ALL must hold)

- Project uses Django 5.x (or 4.2 LTS) with Python 3.12+.
- Code in question lives under `apps/<app>/` or `core/` per the django-coding-standards layout.
- A test runner is configured (`pytest + pytest-django`).
- The team has agreed to enforce service-layer logic separation.

## Skip If (ANY kills it)

- Project is not on Django (FastAPI, Flask, or other) — load the framework-specific methodology instead.
- Tiny throwaway tool with no growth horizon — overhead exceeds payoff.
- Codebase has not adopted the apps/core/config layout and refactoring it is out of scope right now.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `pyproject.toml` | TOML | repo root |
| `apps/<app>/` layout | directory tree | repo source |
| Target Django version | string | `pyproject.toml` |
| Existing test runner config | TOML | `pyproject.toml` `[tool.pytest.ini_options]` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-typing` | Type-checker baseline for Django code. |
| `free/dev/software-developer/django-coding-standards` | Layout standard that gates placement of files produced here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules specific to django-imports | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artifact + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Recurring antipatterns with reason | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree from observable inputs to a rule conclusion | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold model/serializer/view/test from spec | sonnet | Mechanical code generation. |
| Design service-layer boundaries | opus | Needs domain judgement. |
| Audit existing code for layering violations | sonnet | Pattern matching with deterministic output. |

## Templates

| File | Purpose |
|------|---------|
| `templates/django_import_lint.py` | Custom lint rule rejecting bare cross-app symbol imports. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-imports.py` | Validates the output record against `02-output-contract.xml`. | After the methodology runs, before publishing the artifact. |

## Related

- [[django-coding-standards]] — see methodology AGENTS.md for context.
- [[django-models]] — see methodology AGENTS.md for context.
- [[django-pytest]] — see methodology AGENTS.md for context.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` keys off the observable inputs documented in Prerequisites and routes to either "run the methodology" (preconditions hold) or "skip and route elsewhere" (preconditions fail). Use it before invoking the methodology, not after.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/django_import_lint.py`

```python
# django_import_lint.py — flag cross-app imports without alias and wildcard imports.
# Usage: python django_import_lint.py path/to/repo
# Exits 1 if violations found. Wire into pre-commit and CI.
import ast
import pathlib
import sys

BAD: list[tuple[str, int, str]] = []


def check(path: pathlib.Path) -> None:
    try:
        tree = ast.parse(path.read_text(), filename=str(path))
    except SyntaxError:
        return
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom):
            continue
        mod = node.module or ""
        # Cross-app: from apps.<other>.<module> import X (direct symbol import)
        if mod.startswith("apps.") and mod.count(".") >= 2:
            tail = mod.split(".", 2)[2]
            if tail in {"models", "services", "constants", "serializers"}:
                app = mod.split(".")[1]
                BAD.append((
                    str(path),
                    node.lineno,
                    f"use `from apps.{app} import {tail} as {app}_{tail}` "
                    f"instead of `from {mod} import ...`",
                ))
        # Wildcard imports
        for alias in node.names:
            if alias.name == "*":
                BAD.append((str(path), node.lineno, "wildcard import banned"))


root = pathlib.Path(sys.argv[1])
for py in root.rglob("*.py"):
    if "/migrations/" in str(py) or "/.venv/" in str(py) or "/node_modules/" in str(py):
        continue
    check(py)

for f, ln, msg in BAD:
    print(f"{f}:{ln}: {msg}")

sys.exit(1 if BAD else 0)
```
