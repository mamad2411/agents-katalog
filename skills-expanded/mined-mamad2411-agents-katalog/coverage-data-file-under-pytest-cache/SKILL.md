---
name: coverage-data-file-under-pytest-cache
description: Move coverage data files into .pytest_cache/.coverage so pytest-xdist worker fragments (.coverage.<host>.<pid>.<random>) end up inside the already-gitignored cache dir instead of polluting the repo root.
category: build
version: 1.0.0
version_origin: extracted
tags: [coverage, pytest-xdist, gitignore, dx]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: pyproject.toml
imported_at: 2026-04-18T00:00:00Z
---

# Coverage Data File Under .pytest_cache

## When to use
You run tests with `pytest -n auto --cov` and end up with dozens of `.coverage.<hostname>.<pid>.<random>` files at the repo root. They look like garbage, accidentally get committed, and clutter `git status`. There's a one-line fix.

## How it works
Set `tool.coverage.run.data_file` to a path inside `.pytest_cache/`. pytest-xdist appends host/pid/random suffixes to whatever you set, so all the fragments land inside the already-gitignored cache directory.

## Example
```toml
[tool.coverage.run]
# With pytest-xdist (-n auto), each worker writes a fragment; put them under
# .pytest_cache/ (already gitignored) instead of .coverage.<hostname>.* at repo root.
data_file = ".pytest_cache/.coverage"
```

Combine with a Makefile clean target that explicitly nukes leftovers from older runs:
```makefile
clean:
    find . -maxdepth 1 \( -name '.coverage' -o -name '.coverage.*' \) -delete 2>/dev/null || true
```

## Gotchas
- `.pytest_cache/` is gitignored by default in most Python templates; verify yours has it.
- If you use `coverage combine` separately (e.g. in CI to merge fragments from parallel jobs), point its input/output paths at the same `.pytest_cache/.coverage` location.
- Doesn't change behaviour for single-worker `pytest --cov` — it just keeps the folder tidy.
