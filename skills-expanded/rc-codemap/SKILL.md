---
name: rc-codemap
description: "Builds and refreshes per-directory codemap.md as a cheap structure map. Use before exploring a large repo. Do not use to trace one bug."
model: sonnet
effort: medium
---

# Codemap

Maintain a hierarchical, per-directory map of the repository so every exploration-heavy task
starts from a written summary instead of re-scanning source. Each significant directory gets a
`codemap.md`; a root `codemap.md` links them. Regeneration is **incremental** — only directories
that changed since the last run are rebuilt.

## Store & staleness

- Maps live as `codemap.md` inside each mapped directory (committed alongside the code).
- State lives at `.rc/codemap/last-commit` (the git SHA at the last generation).
- `scripts/stale.sh [root]` prints the directories that changed since that SHA — or every
  directory when there is no state yet (first build). `scripts/stale.sh --record [root]` records
  the current HEAD after a successful generation. Both **fail open**: on any git problem they
  behave as if everything is stale, which is safe.

## Workflow

1. **Scope.** Run `scripts/stale.sh` to get the stale directories. If it returns everything,
   you're doing a first full build.
2. **Regenerate stale maps.** For each stale directory — skipping vendored/generated dirs
   (`.git`, `node_modules`, `vendor`, build output, fixtures) — read its files enough to
   summarize, then (re)write its `codemap.md` with: the directory's responsibility, its key
   files and their roles, notable patterns, and how it connects to sibling directories. Anchor
   claims to real paths.
3. **Update the index.** Refresh the root `codemap.md` so it links every directory map.
4. **Record state.** Run `scripts/stale.sh --record` so the next run only rebuilds what changes
   after this point.

## Rules

- A codemap is a map, not a copy: summarize roles and wiring; never paste large code blocks.
- Keep each map short and skimmable — a reader should grasp a directory in under a minute.
- Do not map throwaway directories (build output, vendored deps, fixtures, generated code).
- On a first build of a large repo, map top-down: root + top-level directories first, then
  descend only into directories that hold real logic.

## When to read (not generate)

In any task that begins with codebase exploration, **read the relevant `codemap.md` files
first** and fall back to grep/Read only for what the maps don't cover. That is the token-saving
payoff — the maps exist so agents don't re-derive structure every session.

## Error handling

- Not a git repository → `stale.sh` fails open and reports all directories; do a full build and
  skip the `--record` step (nothing to record without git).
- A directory that is pure generated output → skip it; do not write a map you'll never trust.
