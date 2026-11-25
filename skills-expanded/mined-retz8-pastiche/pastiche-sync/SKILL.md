---
name: pastiche-sync
description: Use when refreshing `pastiche/FACT.md` after a design-system upgrade, refactor, or token change — re-runs the extractor and surfaces drift via lint. FACT-only; never touches KNOWLEDGE/WISDOM/config and never walks the user through remediation.
---

# Pastiche — sync

Refresh FACT after the user's DS changes. Extractor regenerates `pastiche/FACT.md`; lint surfaces orphaned tags in KNOWLEDGE/WISDOM. The user remediates manually.

## Preflight

1. Resolve repo root: `git rev-parse --show-toplevel`; on failure, fall back silently to cwd. Print: *"Syncing `<repo-root>/pastiche/FACT.md`."*
2. If `<repo-root>/pastiche/config.yaml` does not exist, stop:
   > `<repo-root>/pastiche/config.yaml` not found. Run `/pastiche-init` first.

## Extract FACT

Shell: `extract-fact` (cwd = `<repo-root>`). It is on PATH via the plugin's `bin/` — do not search for it. Block on completion.

On non-zero exit, print stderr verbatim and stop. Do not run lint — FACT may be stale or unwritten. The extractor's own message (config parse error, missing input file, etc.) is the actionable surface.

On success, the extractor prints `"Wrote pastiche/FACT.md: <N> components, <M> tokens."` to stdout. Forward it as-is.

## Lint self-check

Shell: `pastiche-lint` (cwd = `<repo-root>`). It is on PATH via the plugin's `bin/` — do not search for it. Block on completion.

Forward stdout (summary) verbatim. If exit is non-zero, also forward stderr (violations) verbatim. No reformatting.

Classify the outcome by exit code + stdout shape:
- **Clean** — exit 0.
- **Drift** — non-zero exit, stdout summary present.
- **Crash** — non-zero exit, no stdout summary. The lint script itself broke; this is not user-visible drift.

Sync itself never exits non-zero on lint output. Carry the classification into Close.

## Close

Print exactly one of:

**Clean:**
> Pastiche synced. FACT.md regenerated; no drift detected.
>
> Run `git diff pastiche/FACT.md` to inspect changes.

**Drift:**
> Pastiche synced — FACT.md regenerated, lint surfaced drift (see violations above).
>
> Remediate by editing `pastiche/WISDOM.md` / `pastiche/KNOWLEDGE.md` directly, or use `/pastiche-write-wisdom` / `/pastiche-write-knowledge` to add or replace rules. Run `git diff pastiche/FACT.md` to inspect the FACT changes that triggered the drift.

**Crash:**
> Pastiche synced. FACT.md was regenerated successfully, but the lint script crashed unexpectedly (output above). Report this to the pastiche maintainers.
>
> Run `git diff pastiche/FACT.md` to inspect changes.

Do not invoke another skill. Do not suggest `/pastiche-setup` — it is curation, not remediation.
