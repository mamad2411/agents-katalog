---
name: cs-resync-codebase
description: >
  Re-sync CodeSpring with the real code after building. Independently checks
  whether the features, notes, and PRDs in CodeSpring still match what the code
  actually does now (features drift from their plan once built), then updates
  CodeSpring to match. Read-only on the codebase — it only reads code/git and
  writes to CodeSpring. Use after a feature is finished, or periodically, to
  keep the map from going stale. Triggers, "resync my codebase", "is CodeSpring
  up to date", "check for stale PRDs", "update CodeSpring from the code", "my
  plan drifted from the code".
allowed-tools: Bash(codespring:*) Bash(npx @codespring-app/cli:*) Bash(git:*) Bash(node:*) Bash(curl:*)
metadata:
  author: codespring
  version: "0.1"
---

# Re-sync CodeSpring with the codebase

Once a feature is built, it rarely matches the original plan exactly. This skill checks CodeSpring against the current code and brings the map/notes/PRDs back into line.

**Guardrail: this is read-only on the codebase.** It reads code and git history and writes ONLY to CodeSpring (features, notes, PRDs). Never modify application code from this skill.

Uses: `codespring` skill references (`analyze-codebase.md`, `mindmap-structure.md`, `prd-management.md`, `pitfalls.md`).

## 0. Connect first
`codespring auth status` + `codespring status` (LOCAL project; print it).

## 1. Establish what changed
- Read recent changes: `git log`, `git diff` since the last sync point (or a branch/tag the user names), and the current state of the relevant files. If a GitHub remote is set, the mindmap's `githubUrl` and the repo are the reference.
- Focus on the feature(s) the user built, but scan for new routes, tables, jobs, env vars, and shared systems anywhere.

## 2. Compare code ↔ CodeSpring
For each affected feature, diff reality against what's documented:
- **Features / sub-features** — any new capability in the code not represented as a feature/sub-feature? Any documented one that no longer exists?
- **Notes** — does the "how it works" note still describe the real flow, files, and routes?
- **PRDs** — do the Frontend/Backend PRDs still match? Especially the shared backend contracts (routes, data model, auth/RLS, jobs/cron, storage/buckets, payments/credits, env vars) and the dependency map.
- **Tech stack** — any new dependency/service to add.

## 3. Report first
Summarize as: **up to date / minor tweaks / stale**, with a short list of concrete diffs (each with file/route/table references and a severity). Let the user confirm before large rewrites.

## 4. Update CodeSpring (writes go here, not to code)
- Add/adjust features & sub-features (`codespring feature create --parent ...`, `feature update ...`), keeping the `node-features` count correct (re-parent if flattened — see `pitfalls.md`).
- Refresh notes (`codespring mindmap note ...`).
- Refresh PRDs: regenerate via `cs-create-prd` where a PRD is materially stale, or `codespring prd sync <id> --file` for targeted content updates.
- Update tech stack / project info if needed.

## 5. Confirm
List what was updated in CodeSpring and give the project link. Note anything you intentionally left (e.g. a planned-but-not-built task).

## What good looks like
- CodeSpring reflects what the code actually does now, not just the original plan.
- Drift is reported by severity with exact references before anything is rewritten.
- The codebase was never modified — only CodeSpring was updated.
