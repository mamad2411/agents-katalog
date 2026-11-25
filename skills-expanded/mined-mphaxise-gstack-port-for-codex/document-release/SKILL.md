---
name: document-release
description: Post-ship documentation sync for Codex. Use when shipped changes should be reflected in README, architecture docs, contributor docs, or release notes.
---

# Document Release

Use this skill after implementation or release work when the documentation should be brought back into sync with reality.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Read the relevant diff or shipped change summary.
2. Identify which docs are now stale:
   - `README.md`
   - architecture docs
   - contributor docs
   - runbooks
   - changelog or release notes
3. Update only the docs actually affected by the change.
4. If a durable release artifact is useful, save it via the `reports` pattern.

## Guardrails

- Do not invent docs the repo does not use.
- Prefer correcting stale statements over rewriting everything.
- Keep documentation aligned with the actual shipped behavior, not the aspirational future.
