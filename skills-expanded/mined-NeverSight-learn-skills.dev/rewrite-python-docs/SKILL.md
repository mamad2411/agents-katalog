---
name: rewrite-python-docs
description: Rewrite Python docs and docstrings from source code. Use when Codex needs to refresh the docs.
---

# Rewrite Python Docs

Use source code as the source of truth. Treat existing docs, docstrings, tests, and examples only as weak hints.

## Guidelines

- Run `scripts/gen-ref-pages.py` to regenerate reference pages under `docs/reference/`. The script will output a navigation table that can be copy-pasted into `zensical.toml`.
- Files to update:
  - docstrings in source code
  - `docs/` (excluding generated `docs/reference/`)
  - description in `pyproject.toml` and `zensical.toml`
  - inventories in `zensical.toml` if needed
- DO NOT EDIT:
  - generated reference pages under `docs/reference/`
- Existing docs, docstrings, tests, examples may be rough, missing, incomplete or misleading, it only serves as weak hint.
- Favor bold, comprehensive rewrites over minor or incremental edits.
- Keep docs concise, fluent, example-first.
- Source code is the source of truth.
- Use Google style docstrings. Read [google-style.md](./references/google-style.md) for details.
- Use markdown in docstrings:
  - Use single backticks for inline code, NOT double backticks.
  - Cross-references are written as Markdown reference-style links: [`Object 1`][full.path.object1].

## Suggested Layout

```text
docs/
  README.md
  getting-started/
    ...
  guides/
    ...
  concepts/
    ...
  reference/  # generated, DO NOT EDIT
    package/
      README.md
      submodule.md
  advanced/
    ...
```

- Keep only the sections the project needs.
- Keep navigation shallow.

## mkdocstrings Notes

- The project uses `zensical` with `mkdocstrings`.
- The `__init__` method is merged into the class' signature and docstring.
- The first line in `__init__` methods' docstrings is ignored.

## Validation

- Run `rumdl fmt .`. Treat its findings as weak hints, not strong constraints.
- Run `mise run lint`.
- Run `mise run docs:build`.
- If validation fails for unrelated reasons, separate those failures from the docs change and report them clearly.
