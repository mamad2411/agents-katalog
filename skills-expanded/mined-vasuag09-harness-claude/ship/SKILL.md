---
name: ship
description: Final pre-merge step — sync docs, then prepare a clean commit/PR summary. Use after verify passes. Does NOT commit or push unless you explicitly ask; it prepares everything and stops.
---

# /ship — docs sync & merge prep

Goal: leave the change merge-ready, with docs in sync and a clear summary — without
performing git actions you didn't ask for.

## Do this
1. **Docs sync** — update **every** doc the change touches, not just the spec. Remove stale
   references; keep docs lean and accurate. Before a release, sweep for anything the change made
   stale and reconcile it **before** committing, not after:
   - **Counts & inventories** — any README/manifest that tallies features (components, commands,
     endpoints, supported versions) must include what you added; reconcile against the source of
     truth, don't eyeball it.
   - **Version & status docs** — bump version manifests; flip roadmap/changelog/status entries to
     match what actually shipped.
   - **Reference docs** — API/config/usage docs and the spec's own status + acceptance-criteria
     checkboxes.
   - **Doc shape & examples** — keep the four doc kinds distinct (tutorial · how-to · reference ·
     explanation); don't blur a reference into a tutorial. **Every code example you add or touch
     must actually run** — paste-and-execute it, don't trust it by eye.

   (Project-specific files to touch live in the project's own context — for this repo, see
   CLAUDE.md → "Release docs sweep".)
2. **Change summary** — assemble from the full diff (`git diff <base>...HEAD`), not just
   the last edit:
   ```
   ## Summary — what & why
   ## Changes (grouped by area)
   ## Test plan — how it was verified (link the /verify evidence)
   ## Risks / follow-ups
   ```
3. **CI readiness** — confirm build, types, lint, tests are green locally; no secrets,
   no debug logs, no `--no-verify`.

## Git boundary (important)
Do **not** run `git commit`, `git push`, or open a PR unless the user explicitly asks — and
create no new branches here (the feature branch already exists, made at first write per
`rules/git.md`). Prepare, then stop:
- **Commit message** in Conventional Commits v1.0.0 form: `type(scope): imperative subject
  ≤72 chars`, `BREAKING CHANGE:` footer when applicable (see `rules/git.md`).
- **PR path**: push the feature branch with `-u`, open the PR (draft until verify passed),
  **squash-merge by default** — merge-commit only if the project's own history shows
  non-squash merges.
- Report "ready to commit/PR — say the word."

## Exit criterion
Docs synced, summary drafted, checks green. Awaiting the user's go for any git action.
