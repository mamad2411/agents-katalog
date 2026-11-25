---
name: openspec-init
description: Initialize or repair OpenSpec in the current repo for the /la:pr flow. Ensures the openspec CLI is available (global install, npx fallback), scaffolds openspec/ with `openspec init --tools none` (corpus only, no /opsx:* commands), and verifies. Invoked by /la:pr when openspec/ is absent or invalid, or run directly.
---

Bring the current repo to a valid OpenSpec state: the `openspec` CLI resolvable
and an `openspec/` corpus (`specs/` + `changes/`) present and healthy. Corpus
only — no `/opsx:*` slash commands or AGENTS wiring, because the `/la:pr` flow
replaces propose/apply.

## Step 1 — Resolve the CLI (set `OPENSPEC_CMD`)

1. If `command -v openspec` succeeds → `OPENSPEC_CMD=openspec`.
2. Else install globally: `npm i -g @fission-ai/openspec` (no sudo where the npm
   global prefix is user-writable — nvm/fnm/`~/.local`-style node). Re-check
   `command -v openspec`.
3. If the global install fails (non-writable prefix, no permission, or offline):
   fall back to `OPENSPEC_CMD="npx -y @fission-ai/openspec@1.11.0"` (bump the pin
   as needed). If even npx can't fetch, STOP and tell me — do not proceed.

Use `$OPENSPEC_CMD` for every openspec call below and hand it back to the caller.

## Step 2 — Check repo state

Run from the repo root (`init` writes `openspec/` into the cwd). Classify:

- **Absent** — no `openspec/config.yaml` → Step 3.
- **Healthy** — `openspec/config.yaml` exists and `$OPENSPEC_CMD list` runs
  cleanly → nothing to do; report and return. (A healthy repo may have no
  `specs/` or `changes/` yet — see Step 3 — so their absence is NOT invalid.)
- **Invalid** — `openspec/` exists but has no `config.yaml`, or `list`/`doctor`
  errors → Step 4.

## Step 3 — Initialize (absent)

```
$OPENSPEC_CMD init --tools none --no-animation
```

Add `--force` only if it complains about legacy files. This creates just
`openspec/config.yaml` (`schema: spec-driven`); `--tools none` keeps it
corpus-only (no `/opsx:*` commands or AGENTS wiring — `/la:pr` gets its authoring
format from `openspec instructions`). Note: `changes/<id>/` is created later by
`openspec new change`, and `specs/` by the first `openspec archive` — init alone
lays down only `config.yaml`.

## Step 4 — Repair (invalid)

- Version / instruction staleness → `$OPENSPEC_CMD update`.
- Structurally broken (missing `specs/`|`changes/`, unparseable corpus) → report
  the exact `doctor`/`list` error and ask how to proceed. Never guess-fix a
  corrupted corpus.

## Step 5 — Verify and stage

- Confirm health: `$OPENSPEC_CMD list` must succeed (and
  `$OPENSPEC_CMD validate --strict` if any specs/changes already exist).
- Stage with a SPECIFIC path — `git add openspec/` plus any other newly created
  files — never `git add -A`. Do NOT commit; leave that to me.
- Worktree caveat: `openspec/` lives on the branch, so init on the mainline (then
  merge) if you want every future branch/worktree to inherit it — don't init
  per-worktree.

Return to the caller (e.g. `/la:pr`) with OpenSpec now valid.
