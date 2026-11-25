---
name: python-stub-package
description: Generate a condensed structural overview of a Python package or module — signatures, imports, class attributes, and docstrings only, with function bodies replaced by ellipsis.
user-invocable: true
license: MIT
compatibility: Designed for Claude Code or similar AI coding agents, and for projects using Python.
metadata:
  author: honnibal
  version: "1.0.0"
  openclaw:
    emoji: "\U0001F4CB"
    homepage: https://github.com/honnibal/claude-skills
---

# Stub Package: Structural Overview Generator

Generate a condensed structural overview of a Python package or module — signatures, imports, class attributes, and docstrings only, with bodies replaced by `...`.

## Usage

Run the stub generator on the target path:

```bash
python stub_package.py <path> [flags]
```

Available flags:
- `--no-docstrings` — omit docstrings (much more compact)
- `--no-private` — skip `_private` names (keeps `__dunder__` methods)
- `--output FILE` — write to a file instead of stdout

## What the output shows

The stub generator parses Python source with `ast` and emits:

- Module docstrings
- Import statements (verbatim)
- Module-level assignments (`__all__`, constants, type aliases)
- Class definitions with bases, decorators, class-level attributes, and method signatures (bodies replaced with `...`)
- Function/async function signatures with decorators (bodies replaced with `...`)
- Source location comments (`# file:line-line`) before each definition

For packages (directories), files are grouped under `# === path/file.py ===` headers, with `__init__.py` listed first.

## The stub_package.py Script

The script is included alongside this skill. It requires Python 3.9+ (uses `ast.unparse`).

## Cross-References

- `python-code-quality` — type hints, module organization
- `python-documentation` — docstrings
