---
name: kos-workflow-health-optimization
description: Run the workflow-health-optimize phase loop (ASSESS/PLAN/EXECUTE) using ONLY the provided Completed Runs Data JSON — never git/gh/curl/network — and edit at most 3 .github/workflows/ files with minimal diffs; do not commit/push.
user-invocable: true
when_to_use: "When the workflow-health-optimize workflow runs its scheduled collect→optimize→report cycle, or when a run failed at report-blocked-gate/report-failure."
category: utilities
argument-hint: "[workflow-name or 'all']"
keywords: [workflow-health, optimize, completed-runs-data, no-gh, phase-based, blocked-gate, asess-plan-execute]
related: [kos-zai-agent-runtime-contract, kos-gh-automation-tooling, kos-zai-run-failure-prevention, kos-claude-turn-budget]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from workflow-health-optimize.yml prompt (GLOBAL CONSTRAINT: no git/gh/curl/network)
  license: repo
  version: "1.1"
---

# Idea

`workflow-health-optimize` runs a phase-based loop (ASSESS → PLAN → EXECUTE) over **pre-collected run data passed in the prompt** (Completed Runs Data JSON, including `claudeSummary`, `timingSummary`, `duplicateSameSha`). **GLOBAL CONSTRAINT: do NOT run `git`, `gh`, `curl`, or any network/API in any phase.** Use ONLY the provided JSON — no log fetching, no run statuses, no issue details from the API. Edits are confined to `.github/workflows/`, max 3 files, minimal (5–10 line) diffs; no commit/push.

## When to invoke this skill directly
- Running the health-optimize cycle.
- Deciding which workflow file to optimize and how — from the provided data only.

## References
- `workflow-health-optimize.yml` prompt (the phase loop + GLOBAL CONSTRAINT + scope).
- Provided inputs: `${{ needs.collect-runs.outputs.runs-data }}` (the only allowed evidence source).
- [[kos-zai-agent-runtime-contract]] — do NOT run disallowed tools; the prompt forbids gh/git/network.
- `report-failure` action (only if the optimization itself genuinely failed).

## Communication Style
Per-workflow health from the provided data → the one bottleneck → the one YAML change (cited to the data) → blocked list.

## Core Principles
YAGNI / KISS / DRY. Provided-data only — never fetch. One bottleneck, one minimal YAML fix. A reporting-step non-zero exit ≠ a failed optimization.

## Cron Collision Detection (WHO-E02)

Part of Phase 1 ASSESS. Proactive - detects runner-load collisions before they manifest as slow/failed runs.

### Method
1. `Grep` for `cron:` in `.github/workflows/*.yml` to collect all scheduled workflows.
2. Parse each cron into minute/hour/dayOfMonth/month/dayOfWeek.
3. **Collision window:** same 5-minute window on same hour/day pattern. Severity: HIGH (both hourly), MEDIUM (hourly + less frequent), LOW (both infrequent).
4. Pair-specific safe offset: `issue-catch-up` `:37` is staggered relative to `workflow-health-optimize` `:07` (do NOT shift `:37` for that pair); `:37` still collides with `pr-flow-watchdog` — see the HIGH collisions list.
5. Report under `CRON COLLISIONS:` in output.

### Stagger Proposal Rules (PLAN phase)
- Shift the less critical workflow minute by +/-5-10 minutes.
- Preserve semantic offsets (`:07`, `:37`, `:56`).
- Never propose minute `0`. Never propose a minute that collides with another schedule.
- Max one cron offset change per cycle.

## Phase loop (enforce)

**GLOBAL CONSTRAINT (all phases):** do NOT run `git`/`gh`/`curl`/network. Use ONLY the provided Completed Runs Data. Do NOT fetch logs, run statuses, or issue details.

- **Phase 1 — ASSESS (turns 1–3):** read the runs data. Also `Grep` for `cron:` in `.github/workflows/*.yml` and detect collisions (see Cron Collision Detection above). Any failures? Slow runs? Use `timingSummary` for queue/runner/job/step bottlenecks (missing timing → mark slow run ambiguous). If a slow successful run is explained by `duplicateSameSha` and CI no longer subscribes to `ready_for_review`, treat that class as already addressed — don't edit. If **ALL runs successful AND none exceeded 5 min → EXIT NOW, no changes.** Do not read workflow YAML bodies yet (the cron surface scan with `Grep` above is allowed; full YAML analysis is Phase 2).
- **Phase 2 — PLAN (turns 4–6):** read ONLY the relevant workflow file(s) per problem. Fixable via YAML? If not → skip. For cron collisions, propose stagger offsets per Stagger Proposal Rules. If the provided data lacks enough detail for a concrete YAML fix → mark ambiguous, skip. If total edits > 3 files → STOP, exit with notes, don't edit.
- **Phase 3 — EXECUTE (remaining turns):** apply planned changes; validate YAML after each edit using only local tools (`node`, `npx`, file reads). Do NOT commit or push.

## Scope (enforce)
- ONLY modify `.github/workflows/` files. Max 3 files per run. Minimal diffs (5–10 lines), not rewrites.
- Do NOT refactor to shared actions (separate task). Do NOT change files outside `.github/workflows/`.

## Failure modes to avoid
- **Running gh/git/curl** — forbidden by the GLOBAL CONSTRAINT; the data is pre-collected.
- **Vibe optimization** — no provided-data evidence; always cite the JSON.
- **Over-editing** — >3 files or rewriting instead of minimal diffs.
- **Misreading a reporting non-zero exit** — report-blocked-gate/report steps may tolerate non-zero (pre-auth); confirm a real error before declaring failure.

## Process Flow (Authoritative)
1. ASSESS provided data + cron collision scan → bottleneck (or all-success/<5min → exit).
2. PLAN → YAML fix per problem incl. cron offset if collision (skip ambiguous; stop if >3 files).
3. EXECUTE → minimal YAML edits; validate each.
4. report-blocked-gate (accurate); report-failure only on a real optimization failure.

## Output Format
```text
HEALTH (from provided data): <wf>: s/f/c/dur … => BOTTLENECK: <wf> (<reason, cited to timingSummary/claudeSummary>)
CRON COLLISIONS: <none|collision list with severity>
OPTIMIZE: <one minimal YAML change> (file: <wf.yml>)
BLOCKED: <none|list>
NETWORK/GH/GIT: not used (per GLOBAL CONSTRAINT)
```

## Critical Constraints
- NEVER run git/gh/curl/network — provided data only.
- One minimal YAML fix per cycle, max 3 files, `.github/workflows/` only.
- Never file report-failure for a tolerated reporting-step non-zero exit.
