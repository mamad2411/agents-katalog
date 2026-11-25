---
name: kos-commit-and-push-branch
description: Reference for the workflow's commit-and-push / upsert-PR STEP (the action that runs after the zai agent) — what it does, how it fails (git_push_403, empty diff, non-fast-forward, graphql_pr_fail), and how to diagnose. Agents do NOT push.
user-invocable: true
when_to_use: "When diagnosing a run that failed at the 'Commit and push' / upsert-PR step, or when reasoning about why an agent's edits did or did not land."
category: utilities
argument-hint: "[run-id or branch]"
keywords: [commit-and-push, upsert-pull-request, git-push-403, workflow-step, bot-identity, automation-pr, no-push]
related: [kos-zai-agent-runtime-contract, kos-zai-run-failure-prevention, kos-gh-automation-tooling]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from fix-review/code-review commit-and-push step failures + commit-and-push/prepare-automation-branch actions
  license: repo
  version: "1.1"
---

# Idea

In these workflows, **the agent does not push.** The zai/agent run only edits files and returns the prompt's output; then a **workflow step** (`commit-and-push`, `prepare-automation-branch`, `upsert-pull-request`) commits the agent's diff and pushes/opens the PR. That step is a frequent failure point — and because it runs *after* the agent, its failure is often misread as an agent problem. This skill is the reference for understanding/diagnosing that **workflow step**, not an instruction for the agent to push. (Agent push discipline lives in [[kos-zai-agent-runtime-contract]].)

## When to invoke this skill directly
- A run failed at the "Commit and push to the PR branch" / upsert-PR step.
- You are reasoning about why an agent's edits did or did not land (empty diff? non-fast-forward? 403?).
- You are editing a workflow's commit-and-push / upsert-PR steps.

## References
- `.github/actions/setup-bot-git/` — sets bot identity (must run before the step).
- `.github/actions/prepare-automation-branch/` — creates/switches the automation branch.
- `.github/actions/commit-and-push/` — staged commit + push (the recurring failure point).
- `.github/actions/upsert-pull-request/` + `find-duplicate-automation-pr.cjs` — open/reuse the PR.
- `scan-claude-logs.cjs` → `git_push_403`, `graphql_pr_fail`.

## Communication Style
Name the exact step, the one cause (token/identity/non-fast-forward/empty), and that it is a workflow-step (not agent) failure.

## Core Principles
YAGNI / KISS / DRY. Diagnose the step, don't blame the agent. The fix lives in the workflow YAML (token, identity, gate), not in agent cleverness.

## Step-failure causes → diagnosis

| Symptom | Cause | Where the fix lives |
|---|---|---|
| `fatal: unable to access … 403` (`git_push_403`) | Push token lacks `contents: write` / wrong remote | workflow: use `GH_PAT`; `setup-bot-git` remote |
| `Commit and push … failure` (generic) | No bot identity, or staged nothing | workflow: `setup-bot-git` before; guard step with `if: git diff` |
| `! [rejected] non-fast-forward` | Branch moved under the agent | workflow: rebase/reprepare branch (rebase-pr flow) |
| `pull request create failed: GraphQL:` (`graphql_pr_fail`) | Duplicate PR / transient | workflow: `find-duplicate-automation-pr.cjs` + `upsert-pull-request` |
| Push of an empty tree | Agent made no net change | workflow: `detect-noop` → skip gate+push, post `renderNoChanges` (see fix-review §6d) |

## Your Approach (diagnosis)
1. Confirm the failure is at the commit-and-push/upsert **step** (after the agent), not during the agent run.
2. Map the symptom to a row above.
3. Point the fix at the workflow YAML/step, not the agent.
4. Note: an empty agent diff is a workflow `detect-noop` success-with-no-changes, not a step failure.

## Process Flow (Authoritative)
1. Identify the failing step + the agent's preceding diff (was there one?).
2. Classify the step failure (403 / identity / non-fast-forward / graphql / empty).
3. Recommend the workflow-level fix; confirm the agent's own behavior was correct.

## Output Format
```text
STEP: <commit-and-push|upsert-PR>  CAUSE: <403|identity|non-fast-forward|graphql|empty-diff>  FIX-LOC: <workflow step>
```

## Critical Constraints
- This skill never instructs an agent to push — agents edit files only ([[kos-zai-agent-runtime-contract]]).
- An empty diff is a clean no-op (workflow `detect-noop`), not a failure.
- Distinguish step failures from agent-runtime failures (`kos-zai-run-failure-prevention`).
