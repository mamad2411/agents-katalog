---
name: github-actions-workflow-dispatch
description: Base skill — trigger a GitHub Actions `workflow_dispatch` run via the `gh` CLI, optionally polling until the newly-spawned run reaches completed status. Pure stdlib Python wrapper. Distinct from `github-actions-run-audit` (observation-only) and `github-workflow-creation` (authoring).
category: GitHub-Automation
---

# GitHub Actions Workflow Dispatch Skill (v1)

> **Skill ID:** `github-actions-workflow-dispatch`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base (per [`skill-factory` §2.0 Layering Decision](../skill-factory/SKILL.md))

## 1. When to Apply

Use this skill — or a higher-level composer of it — whenever the agent must
**actively trigger** a GitHub Actions workflow run (a write action), such as:

- "Re-run the periodic backup workflow NOW because we made a schema change."
- "Kick off the deploy pipeline against branch `<X>` with input `env=prod`."
- "Manually fire the docs-regen workflow and wait for completion before
  proceeding with the next plan step."

**Anti-trigger:** If the agent only wants to **observe** existing runs, use
[`github-actions-run-audit`](../github-actions-run-audit/SKILL.md) — that
skill is read-only and safer.

## 2. Why a separate skill (vs folding into audit)

Auditing (observation) and dispatching (action) are different concerns:

| Concern | Audit | Dispatch |
| --- | --- | --- |
| Side effects | None | Spawns a new run, consumes minutes |
| Permissions needed | `actions:read` | `actions:write` |
| Safe-by-default | Yes | No — requires user authorization |
| Re-runnable | Yes | No — duplicate runs may be undesirable |

Per the [Layered Composition Mandate](../../../ai-agent-rules/ai-rule-standardization-rules.md),
each primitive owns its own SSOT.

## 3. Required Inputs

- `gh` CLI installed and authenticated with `actions:write` on the target
  repo (`gh auth status` clean; `gh auth refresh -s workflow` if needed).
- Workflow must declare `on: workflow_dispatch:` in its YAML.
- Python 3.10+ on PATH (sourced via `mise` per workspace convention).

## 4. Operational Logic

### 4.1 Script catalogue

| Script | Purpose | Required args | Behavior |
| --- | --- | --- | --- |
| [`scripts/trigger-workflow.py`](scripts/trigger-workflow.py) | Wrap `gh workflow run`, optionally poll `gh run list` until the new run reaches `status == completed`. | `--repo`, `--workflow` | Fire-and-forget by default; pass `--wait <seconds>` to block until completion. Emits JSON `{repo, workflow, triggered, run?, timed_out?}`. |

### 4.2 Invocation patterns

```bash
SCRIPTS_DIR=.agents/skills/github-actions-workflow-dispatch/scripts

# Fire-and-forget
python3 "$SCRIPTS_DIR"/trigger-workflow.py --repo owner/repo --workflow my-workflow.yml

# Trigger and wait up to 5 minutes; non-zero exit on timeout
python3 "$SCRIPTS_DIR"/trigger-workflow.py --repo owner/repo --workflow my-workflow.yml --wait 300

# With inputs and a non-default ref
python3 "$SCRIPTS_DIR"/trigger-workflow.py --repo owner/repo --workflow deploy.yml \
    --ref release/v2 --field environment=prod --field debug=false --wait 600
```

### 4.3 Polling semantics

- The script snapshots the existing `databaseId` set BEFORE dispatch, then
  polls every `--poll <seconds>` (default 10) for a run with a new id.
- When the new run reaches `status == completed`, the script prints its JSON
  and exits 0 — regardless of `conclusion` (success / failure / cancelled).
  The caller is responsible for inspecting `conclusion`.
- Timeout (`--wait <s>` exceeded) prints the in-progress run JSON and exits 1.

### 4.4 Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Triggered (and, when `--wait > 0`, completed) |
| `1` | `gh` missing, dispatch failed, or `--wait` timed out |
| `2` | Config error (missing `--repo` / `--workflow`) |

## 5. Composition by Higher-Level Skills

| Composer | Uses | Purpose |
| --- | --- | --- |
| [`github-actions-run-audit`](../github-actions-run-audit/SKILL.md) | `trigger-workflow.py` | "Trigger then audit" combined workflow (e.g., re-run periodic backup, wait, then verify the committed artifact). |
| [`db-backup-bracketing-protocol`](../db-backup-bracketing-protocol/SKILL.md) | `trigger-workflow.py` (via §Step 1 dispatch+watch) | Pre+post / post-only / none bracket patterns around destructive DB operations, with recovery-anchor logging. |

## 6. Composition by This Skill

This skill composes with:

- [`github-rest-api-fallback`](../github-rest-api-fallback/SKILL.md) —
  REST equivalent (`POST /repos/{o}/{r}/actions/workflows/{id}/dispatches`)
  when `gh` is unavailable.
- [`github-workflow-creation`](../github-workflow-creation/SKILL.md) — the
  AUTHORING-side counterpart that decides which workflows even have
  `workflow_dispatch` enabled.
- [`mise-tool-management`](../mise-tool-management/SKILL.md) — interpreter
  pinning.

## 7. Prohibited Behaviors

- Triggering a workflow without explicit user authorization. Dispatch is a
  write action — the agent MUST ask before firing.
- Polling without a deadline (`--wait 0` + custom loop in caller code) —
  always set a bound to avoid runaway agent loops.
- Triggering against `main` / `master` when the user intended a feature
  branch — always confirm `--ref` when in doubt.
- Re-triggering a workflow that just failed without first auditing WHY it
  failed — use [`github-actions-run-audit`](../github-actions-run-audit/SKILL.md) first.
