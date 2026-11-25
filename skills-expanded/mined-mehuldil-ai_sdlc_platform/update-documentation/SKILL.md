---
name: update-documentation
description: Atomic doc update — align README, wiki paths, ADRs, and User_Manual when behavior or contracts change
model: sonnet-4-6
token_budget: {input: 4000, output: 2000}
---

# Update Documentation

**Purpose:** One place to describe **what** to update when code or gates change, so product/backend/frontend agents do not each invent a different doc process.

## When to invoke

- Public API, CLI flag, or **gate** behavior changed
- **PRD / story** text must match shipped behavior
- **ADR** required for a design decision (see `rules/gate-enforcement.md`)

## Steps

1. **Inventory** — List affected surfaces: `README*`, `User_Manual/*`, `docs/`, stack `rules/`, ADR under `.sdlc/memory/` or `docs/adr/`.
2. **Scope** — Update only what the change touches; link PRD-REF / AB# in commit or PR per `rules/traceability-pr-prd.md`.
3. **Normalize** — For non-Markdown sources, run **`skills/shared/doc-normalizer/SKILL.md`** first.
4. **Verify** — Run `sdlc doctor` or `bash scripts/detect-doc-drift.sh` when available in the consuming repo.

## Do not

- Duplicate long prose already in **`rules/`** — link instead.
- Update the public mirror-only tree; **`ai-sdlc-platform`** is the authoring repo per `REPO_LAYOUT.md`.
