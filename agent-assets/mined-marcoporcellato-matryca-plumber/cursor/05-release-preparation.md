---
description: Prepare a semver release (CHANGELOG, pyproject.toml, uv.lock, checks)
alwaysApply: false
---

# Release preparation (Matryca Plumber)

When the user asks to **prepare**, **cut**, or **ship** a release (e.g. “prepare release v1.6.2”, “rilascia 1.6.2”), run this checklist **in order** without skipping steps.

## Inputs

- Target version: `X.Y.Z` (from user message; accept `vX.Y.Z` and normalize).
- Today’s date: ISO `YYYY-MM-DD` for the changelog heading.

## Steps

1. **Read** `CHANGELOG.md`. Under `## [Unreleased]`, there must be at least one meaningful bullet **or** the user explicitly confirms an empty/maintenance release.
2. **Finalize changelog**
   - Rename `## [Unreleased]` → `## [X.Y.Z] - <today>`.
   - Insert a fresh `## [Unreleased]` at the top (after the intro lines) with empty optional subsections or none.
3. **Bump version** — set `version = "X.Y.Z"` in `pyproject.toml` (no `v` prefix).
4. **Lockfile** — run `uv lock` from the repo root.
5. **Verify notes** — run `python scripts/extract_changelog.py vX.Y.Z` and confirm output matches the new section.
6. **Tests** — run `make check` if available; otherwise `uv run ruff check src tests`, `uv run mypy src tests`, `uv run pytest -q`.
7. **Summarize for the user** — list changed files and the exact git commands from `docs/RELEASE_PROCESS.md` (commit message `chore: release X.Y.Z`, tag `vX.Y.Z`, push branch + tag). **Do not** create the tag or push unless the user explicitly asks.

## Constraints

- Never tag `[Unreleased]` or ship with version/changelog mismatch.
- Do not use `gh release create --generate-notes`; release notes come only from `CHANGELOG.md` via CI.
- Do not commit secrets (`.env`).
- Only create a git commit when the user explicitly requests it.

## Reference

- [`docs/RELEASE_PROCESS.md`](docs/RELEASE_PROCESS.md)
- [`scripts/extract_changelog.py`](scripts/extract_changelog.py)
