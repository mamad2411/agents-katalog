---
name: kos-run-monitoring
description: Monitor recent GitHub Actions runs via rtk gh, detect failures, diagnose root cause, and (per the prompt) apply ONLY narrow evidence-backed fixes — never push/merge/PR; the workflow handles those.
user-invocable: true
when_to_use: "When the monitor-amnezia-control-panel-github-runs workflow surveys recent runs and may apply narrow fixes, or when standing up/repairing its diagnose-then-report flow."
category: utilities
argument-hint: "[window or workflow]"
keywords: [monitor, runs, github-actions, detect, diagnose, rtk-gh, narrow-fix, no-push]
related: [kos-zai-agent-runtime-contract, kos-run-log-mining, kos-gh-automation-tooling, kos-zai-run-failure-prevention, kos-claude-turn-budget]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from monitor-amnezia-control-panel-github-runs.yml (/gsd:debug) prompt + 30/30 success runs
  license: repo
  version: "1.1"
---

# Idea

`monitor-amnezia-control-panel-github-runs` watches recent runs across workflows, detects failures/slow runs/bottlenecks, diagnoses each with exact GitHub evidence, and — when the evidence is unambiguous — may apply **narrow, evidence-backed, safe** workflow/helper fixes. It is **not** pure diagnose-only, but it **never** commits/pushes/merges/opens a PR (the workflow handles those). It is the most reliable workflow (30/30) because it stays evidence-first.

## When to invoke this skill directly
- Running the monitor sweep.
- Detecting + diagnosing a batch of recent failures.

## References
- `monitor-amnezia-control-panel-github-runs.yml` prompt (`/gsd:debug`; `rtk gh run list/view`; `rtk proxy gh run view --log-failed`; narrow evidence-backed fixes only; **do not commit/push/merge/PR**; do not migrate `$CODEX_HOME` memory; uses GitHub run history as memory).
- [[kos-run-log-mining]] — layered diagnosis (rollup → reason → surgical grep).
- `.github/workflows/scripts/analyze-claude-runs.sh` + `scan-claude-logs.cjs`.
- [[kos-zai-agent-runtime-contract]].

## Communication Style
Rollup → failed/slow runs with evidence → narrow fix (if unambiguous) or report (if ambiguous). No push.

## Core Principles
YAGNI / KISS / DRY. Evidence before conclusion (never infer from run names/conclusions alone). Narrow fixes only; ambiguous → no changes, report. Never push. Transient (rate-limit/cancel) ≠ actionable.

## Your job (enforce)
1. **Survey** runs since MONITOR_SINCE (+ recent failed/slow since RECENT_PROBLEM_SINCE) via `rtk gh run list` (required fields) and `rtk gh run list` again for candidates.
2. **Evidence:** for each actionable failed run, `rtk gh run view <id> --json … --verbose` + `rtk proxy gh run view <id> --log-failed` (use `--log` if incomplete); for slow runs, `rtk gh run view <id> --json jobs,…`. Do **not** infer root cause from names/conclusions alone.
3. **Diagnose** each to a dominant mode + evidence ([[kos-run-log-mining]]).
4. **Act** only on unambiguous evidence: apply a narrow, safe, shared workflow/helper fix. If evidence is ambiguous → make no file changes, report what was inspected.
5. **Verify** changes: JS/CJS/TS/TSX → `npm run lint` + targeted `npx prettier --check`; workflow/action YAML → `actionlint -config-file .github/actionlint.yaml` + prettier --check; shell → `shellcheck`.
6. **Never** commit/push/merge/PR. Do not read `$CODEX_HOME/automations` memory.

## Failure modes to avoid
- **Inferring from run names/conclusions** — read exact logs first.
- **Broad fixes** — narrow + shared + evidence-backed only.
- **Pushing** — forbidden; the workflow handles Git/PR.
- **Re-reading full logs** — use `--log-failed` + grep.
- **Treating cancel/skip as failure** — cancel ≈ supersession; skip ≈ trust gate.

## Process Flow (Authoritative)
1. Survey runs (`rtk gh run list`).
2. Gather exact evidence per actionable run.
3. Diagnose (dominant mode + evidence).
4. Narrow fix only if unambiguous; else no changes + report.
5. Verify per file type.
6. Summarize runs inspected + evidence + changes (or no-change rationale). Do not push.

## Output Format
```text
SURVEY: <n> runs across <m> workflows
FAILURES/SLOW: #<id> <wf> => <mode> (<evidence>) [fixable-narrow|ambiguous]
CHANGES: <files> (lint/prettier/actionlint/shellcheck ok) | NONE (ambiguous)
PUSH: none (workflow handles)
```

## Critical Constraints
- Never push/merge/PR — the workflow handles those.
- Never infer root cause from run names or conclusions; read exact logs.
- Only narrow, evidence-backed, shared fixes; ambiguous → no changes.
- Do not read `$CODEX_HOME/automations` memory; this workflow uses GitHub run history as memory.
