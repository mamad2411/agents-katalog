---
name: harness-doctor
description: Diagnose recurring coding-agent failures from repository state, diffs, logs, tests, progress records, and harness state, then propose or apply the smallest preventive harness change. Use when an agent looped, stopped early, lost context, violated architecture, broke the environment, or left inconsistent task state.
---

# Harness Doctor

Diagnose before editing. A failed run may be a code defect, missing information, unclear acceptance criteria, environment failure, unsafe automation, or an overly restrictive harness; do not assume every failure needs more instructions or hooks.

## Collect read-only evidence

Inspect, when present:

- user request and acceptance criteria;
- current diff and untracked files;
- recent Git history without changing it;
- test, lint, CI, runtime, and browser errors;
- `AGENTS.md`, `CLAUDE.md`, plans, progress, features, and architecture docs;
- `.harness/state/` counters and warnings;
- task locks and their owners and timestamps.

Do not assume conversation transcripts or tool traces exist. Do not read or expose secrets. Treat user changes in a dirty worktree as evidence to preserve.

## Classify the failure

Use concrete categories:

| Failure | Evidence |
|---|---|
| Repeated ineffective edits | Same symptom and file changed repeatedly without a new hypothesis |
| Premature completion | Required behavior was not exercised or evidence contradicts the claim |
| Scope explosion | Unrelated changes or multiple goals mixed into one run |
| Context gap | Required repository fact was unavailable or not consulted |
| Environment gap | Setup, dependency, service, or fixture was missing or unhealthy |
| Architecture drift | A documented, valid boundary was violated |
| State inconsistency | Task status, lock, plan, and code disagree |
| Unsafe automation | A hook or script staged, committed, stashed, reverted, deleted, or contacted external systems without authority |
| Harness friction | Instructions are duplicated, stale, contradictory, or too rigid for the task |

State the causal chain and confidence. Separate root cause from symptoms.

## Select the smallest fix

Examples:

- clarify one acceptance criterion or add an executable regression test;
- add a precise repository-map link instead of expanding global instructions;
- make setup validation explicit and idempotent;
- add a mechanical architecture check for a real boundary;
- reduce or remove a noisy hook;
- reset an inconsistent status only after confirming ownership and current work;
- add a targeted repeated-edit prompt that requests review but never mutates Git.

Do not add blanket “always commit,” “one feature per session,” or model-specific reasoning mandates unless the user has chosen that workflow.

## Recovery safety

Never automatically stash, reset, revert, clean, delete locks, or discard changes. Show the diff and recovery options. Request explicit authorization for any destructive or Git-history-changing action.

## Verify and report

Reproduce the original failure when practical, apply the approved minimal change, and run the relevant check again. Report:

1. observed failure and evidence;
2. root cause and confidence;
3. harness or code change applied;
4. verification result;
5. remaining risks and next action.

Do not commit unless the user asked for a commit.
