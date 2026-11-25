---
name: kos-gh-automation-tooling
description: Map a workflow task to the right reusable .github/actions and scripts (run-zai, report-failure, evaluate-trigger-policy, orchestrate-pr-flow, the classify/evaluate helpers) instead of hand-rolling shell.
user-invocable: true
when_to_use: "When choosing how a workflow should accomplish a step (run the agent, report a failure, gate a trigger, orchestrate PR flow) or when editing a workflow YAML."
category: utilities
argument-hint: "[step you need to perform]"
keywords: [actions, scripts, reusable, orchestrate, report-failure, run-zai, tooling]
related: [kos-zai-run-failure-prevention, kos-commit-and-push-branch, kos-trigger-policy-trust-gate, kos-run-log-mining]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from .github/actions/ and .github/workflows/scripts/ inventory
  license: repo
  version: "1.0"
---

# Idea

The repo has a rich library of composite actions and Node scripts that already implement the hard parts of CI automation. Workflows (and the agents driving them) should **call these**, not reinvent them. Re-deriving this knowledge every run is the #1 wasted-effort pattern. This skill is the map from intent → existing tool.

## When to invoke this skill directly

- You are editing a workflow YAML and about to write inline shell for something an action already does.
- An agent run is about to `gh`/`git` its way through a task that has a dedicated script.
- You need to know which `evaluate-*`/`classify-*`/`collect-*` helper governs a decision.

## References

Key actions (`.github/actions/`):
- `run-zai` — run Claude Code (the agent runtime). Always use this, not raw claude-code-action.
- `setup-environment` — shared first step (node, deps, gsd, rtk, uv flags).
- `setup-bot-git` — bot git identity for commits.
- `report-failure` — open a failure issue + dispatch triage on a red run.
- `ensure-workflow-labels` — create labels from `policy.json`.
- `commit-and-push`, `prepare-automation-branch`, `upsert-pull-request` — PR/branch lifecycle.
- `validate-pr-gate`, `ensure-disk-space`, `ensure-docker-disk-space`, `prettier-auto-fix`.
- `collect-workflow-failure-context` — gather context for a failed run.

Key scripts (`.github/workflows/scripts/`):
- `evaluate-trigger-policy.cjs` (+ `policy.json`) — trust gate.
- `scan-claude-logs.cjs` / `parse-claude-execution.cjs` — run failure taxonomy + metrics.
- `classify-claude-retry.cjs` — retry vs give-up.
- `orchestrate-pr-flow.cjs` — central PR flow brain.
- `evaluate-pr-policy.cjs`, `evaluate-fix-review-eligibility.cjs`, `evaluate-rebase-eligibility.cjs`, `evaluate-pr-finalizer-decision.cjs` — per-flow eligibility.
- `classify-audit-fix.cjs`, `collect-gsd-planning-intake.cjs`, `collect-review-feedback.cjs`, `build-automation-pr-body.cjs`.
- `analyze-claude-runs.sh` — batch run analysis.

## Communication Style

For an intent, return the single action/script to call and its key inputs. Do not paste full YAML.

## Core Principles

YAGNI / KISS / DRY. If an action exists for the step, use it. One tool per intent. Compose actions; don't fork them.

## Intent → tool map

| You need to… | Use |
|---|---|
| Run the Claude agent | `run-zai` (api-key, prompt, max-turns, allowed-tools, allowed-bots) |
| Set up the job | `setup-environment` (first step, always) |
| Report a red run | `report-failure` (mode: issue/ comment; dispatch-triage) |
| Gate a trigger | `evaluate-trigger-policy.cjs` + `policy.json` |
| Decide PR-flow eligibility | `evaluate-pr-policy.cjs` / `orchestrate-pr-flow.cjs` |
| Diagnose a Claude run | `scan-claude-logs.cjs` (outputs `claude_has_findings`, `claude_failure_reason`) |
| Commit + push a fix | `commit-and-push` after `setup-bot-git` |
| Open/reuse automation PR | `upsert-pull-request` + `find-duplicate-automation-pr.cjs` |
| Free runner disk | `ensure-disk-space` / `ensure-docker-disk-space` |
| Analyze many runs | `analyze-claude-runs.sh` |

## Your Approach

1. Name the intent in one phrase.
2. Look it up in the map.
3. Call that action/script with the documented inputs.
4. If nothing fits, check the scripts dir again before writing inline shell.

## Process Flow (Authoritative)

1. State the intent.
2. Resolve to the mapped tool (or confirm none exists).
3. Wire it into the workflow with the right inputs/secrets.
4. Surface the tool's outputs to later steps rather than re-querying.

## Output Format

```text
INTENT: <phrase>  =>  TOOL: <action/script>  INPUTS: <key inputs>
```

## Critical Constraints

- Prefer `run-zai` over any direct claude-code-action call — it owns retries, metrics, scanning.
- Never bypass `report-failure`; a silent red run is worse than a filed issue.
- If two scripts overlap in purpose, use the one the surrounding workflow already uses (consistency over novelty).
