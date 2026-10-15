---
name: desloppify
description: >
  Code quality scanner. Detects AI-introduced anti-patterns across many
  categories. Run the CLI, triage results, fix on isolated git worktrees.
  Trigger: desloppify, clean up code, remove slop, code quality, dead code.
---

# Desloppify

Yes — keep this file lean.

This `SKILL.md` is the operational entrypoint. Put only the workflow and decision points here. Keep detailed command/config/reference material in companion docs and load them only when needed:

- `reference/commands.md`
- `reference/packs-and-tools.md`
- `reference/config-and-plugins.md`
- `reference/overhaul-review.md`

## What this skill is for

Use it when the user wants to:
- desloppify a repo
- clean up AI slop
- run a code-quality pass
- scan for dead code / weak types / complexity / anti-patterns
- run a structured overhaul review or phased cleanup audit

The CLI detects. The agent triages and decides what to fix.

Default behavior is still scan → triage → fix. Only switch into overhaul-review mode when the user clearly wants a broader audit or phased cleanup plan.

## Default workflow

### Optional overhaul-review mode

If the user wants a broader audit instead of an immediate cleanup pass, load `reference/overhaul-review.md` and choose a mode first:
- **Surgical** — one theme only
- **Systematic** — section-by-section review, pause at each section
- **Full audit** — broad phased roadmap

Do not silently switch into overhaul mode for an ordinary desloppify request.

### 0) Set up
Run:

```bash
desloppify check-tools [path]
```

If the repo clearly needs setup help, also use:

```bash
desloppify install-skill
desloppify install-hooks
desloppify setup
```

`install-hooks` scaffolds `.githooks/` into the current git repo and enables it. The installed hooks resolve the CLI from the repo, `bunx`, or PATH; auto-pick the repo's suggested pack when unambiguous; and refuse to clobber unmanaged hook files or replace another active hook chain from `.git/hooks`, `.husky`, or worktree-scoped hook config. Hook runs default to current changes; set `DESLOPPIFY_HOOK_SCOPE=repo` when the user wants hook scans to cover the whole repo.

If you need the exact commands or pack/tool setup details, read:
- `reference/commands.md`
- `reference/packs-and-tools.md`

### 1) Scan
Start with a normal scan for the most relevant pack.

Common default:

```bash
desloppify scan [path] --pack js-ts
```

That default JS/TS path intentionally keeps `madge` off the main run so missing or slow circular-deps analysis does not block ordinary scans. Only add `--with-madge` or `--category circular-deps` when the user explicitly wants circular dependency analysis.

Then read artifacts in this order:
1. `.desloppify/reports/latest.findings.json`
2. `desloppify report [path]`
3. `.desloppify/reports/latest.report.md`
4. `.desloppify/reports/latest.wiki.json` or `.desloppify/reports/latest.handoff.md`

The first artifact-writing scan also auto-adds `.desloppify/` to `.gitignore` in git repos so this state stays local by default.

Use `--json`, `--markdown`, `--wiki`, `--handoff`, `--delta`, or benchmark commands only when the task needs those outputs. On very large repos, prefer `--json --summary` so stdout stays compact while the full artifact is still written to disk. For exact variants, read `reference/commands.md`.

### 2) Triage
For each issue bucket, decide:
- **Fix** — worth changing now
- **Skip** — intentional or low-value churn
- **Flag-only** — public API / dynamic behavior / serialization / risky refactors

Important:
- do not mistake external analyzer warnings for a clean repo
- partial scans skip whole-project analyzers
- full JS/TS scans skip `madge` by default unless you opt in
- `check-tools` can suggest among the shipped `js-ts`, `python`, `rust`, `go`, and `ruby` packs before you scan

If you need pack/tool behavior details, read `reference/packs-and-tools.md`.

### 3) Fix
Prefer isolated worktrees for parallel fix streams:

```bash
desloppify worktrees [path]
```

Then give each fix agent:
1. the worktree path
2. the saved report path or a focused scan slice
3. `desloppify fix . --safe` first
4. a re-scan after edits

Current rule of thumb:
- `fix --safe` is the dependable default
- broader fix tiers are partial and need judgment

### 4) Verify
After fixes:

```bash
desloppify scan [path]
desloppify report [path]
```

Use `desloppify delta ...` when you need regression gating or before/after comparison.

## When to load the companion docs

Load `reference/commands.md` when you need:
- exact CLI invocations
- report / delta / benchmark flows
- artifact paths

Load `reference/packs-and-tools.md` when you need:
- supported packs
- tool adapters
- install commands
- madge / partial-scan / repo-local tool behavior

Load `reference/config-and-plugins.md` when you need:
- config file discovery
- supported config fields
- plugin examples
- `desloppify/plugin-api`
- plugin `rules.<id>.options`
- the stable root programmatic API
- `identityGroup` / `fix` plugin behavior

Load `reference/overhaul-review.md` when you need:
- Surgical / Systematic / Full review modes
- sectioned audit flow
- impact/effort matrix output
- out-of-scope / failure-mode / execution-order summaries

## Guidance for large findings

Treat `GOD_FILE` as a refactor signal, not a blind split command.
Inspect why it tripped:
- too many imports
- mixed route + DB concerns
- barrel/export concentration
- too many HTTP methods in one route file
- too many `useState` calls
- generic bucket-file structure

## Safety tiers

- **T1** — mechanical fixes
- **T2** — AST-validated fixes
- **T3** — cross-file fixes
- **Flag-only** — never auto-fix

## Suppression

Inline:

```bash
console.log("intentional"); // desloppify:ignore CONSOLE_LOG
```

Project-level suppression uses `.desloppifyignore`.
