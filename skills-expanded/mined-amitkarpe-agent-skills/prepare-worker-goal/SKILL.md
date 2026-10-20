---
name: prepare-worker-goal
description: Prepare or revise one bounded persistent-worker goal when the user explicitly requests a delegation plan or goal file. Do not trigger for generic planning, tiny direct tasks, status checks, or execution of an already approved goal; use run-worker-goal for dispatch.
---

# Prepare Worker Goal

Use this skill when the task is not “execute now,” but “prepare the best worker
goal first.”

This skill prepares scope; [run-worker-goal](../run-worker-goal/SKILL.md) handles
approved dispatch. Read the repository's instructions and applicable SPEC first.
Shared policy owns approval, test and lifecycle rules; the vendor adapter owns
model selection. Do not reproduce those policies in every goal.

## Core Behavior

- Think before delegation.
- Read only the minimum repo/live truth needed.
- Use the exact approved lane/goal path; do not create another prompt copy.
- Review the goal critically before it is sent.
- Cite exact existing approval for AWS, stable services, IAM, networking or
  production-like state; ask only when that approval is missing or ambiguous.
- Do not execute the worker unless Amit explicitly asks to run it.
- Do not replace or dispatch over an active goal. Prepare a non-conflicting
  sidecar only when explicitly authorized. Treat UI state as a hint; reconcile
  the current goal/result before selecting a continuation.

## Default Truth Files

Use:

```text
AGENTS.md
CONTEXT.md
```

Avoid `PLANS.md`, `STATUS.md`, and repo-root `GOAL.md` unless the repo has an
explicit exception.

## When To Use Subagents

Use subagents when one or more are true:

- repo truth is spread across multiple large files
- live state and repo state must be compared
- goal needs independent risk/audit review
- multiple facts can be gathered safely in parallel

Do not use subagents for tiny linear tasks.

## Goal Quality Checklist

Before sending a worker goal, confirm:

- one bounded objective
- one verifiable outcome and the shortest existing path to prove it
- which repo-owned workflow is reused, and why any new runner or file is needed
- for code changes, the base revision, intended files, approximate change
  budget and the condition that would require re-scoping
- explicit repo and lane
- explicit read-first files
- allowed mutation
- no-go boundaries
- stop conditions
- success criteria
- evidence path
- done marker path
- cleanup/rollback expectation
- worker model/session expectation when relevant
- whether the worker should use internal subagents
- exact goal ID/revision and `Reply-To`
- cleanup owner, approved durable destination and retention decision

For a POC or MVP, keep the goal and change budget small enough to review as one
proof. If the work needs a new dependency, service, cloud resource, parallel
runner or unrelated UI, reconcile that scope with the owning SPEC and approval
before adding it. Passing tests alone does not justify a new runner when an
existing path can provide the requested proof.

## Worker Status Gate

Before writing or refreshing a worker goal:

1. Read `CONTEXT.md`.
2. Read the exact current marker path named by the goal or private registry.
3. Read the referenced `RESULT.md` only when the marker exists or the context
   points to it.
4. Inspect tmux only if the marker/result is stale or the worker may still be
   running.

Rules:

- Active or uncertain goal: do not overwrite or duplicate it. A separate
  preparation task needs explicit non-conflicting scope.
- Marker `blocked`: prepare a follow-up goal only after the blocker is
  understood and the needed approval/Ops ask is explicit.
- Marker `done safe_to_continue=yes`: reconcile the matching result and
  controller decision before proposing a SPEC-covered next action. The marker
  does not grant new scope or cleanup authority.
- Multiple possible goals: stop and ask for lane/path instead of guessing.
- AWS mutation goal: name the exact applicable approval or the missing decision.
- Do not dispatch here. Use the [native queue protocol](https://github.com/amitkarpe/agent-os/blob/535be4b923cb996d85613d970159d71499ad75ae/kb/playbooks/delegation/codex-native-controller-worker-protocol.md)
  only in an authorized execution step; no composer fallback.

## Goal File Shape

```text
# <lane> goal - <short name>

Controller timestamp:
Goal ID/revision:
Worker role and verified thread:
Reply-To:
Repo:
Exact lane/result/marker paths:
Cleanup owner / durable destination / retention decision:
SPEC and exact approval reference:
Base revision and change budget (for code changes):

Objective:
- <one bounded objective>

Read first:
1. AGENTS.md
2. CONTEXT.md
3. <this goal file>

Allowed mutation:
- <read-only / exact files / one host / one AWS action>

No-go boundaries:
- <what must not be touched>

Phase 0 Probe:
- <checks before mutation>

MVP Proof:
- <smallest proof>

Full Lane only if:
- <gates>

Stop immediately if:
- <blockers>

Success condition:
- <what proves done>

Closeout:
- write RESULT.md
- update done marker
- notify the exact Reply-To using the adopted native queue protocol
- include next safe action and retention obligation
- wait for controller acceptance; cleanup requires separate exact-path authority
```

## Output Contract

For Amit approval, use:

```text
State:
- ...

Recommended:
- ...

Needs approval:
- yes/no, and why

Next command:
- ...
```

After preparing:

```text
Prepared:
- <goal file path>

Worker:
- <session/repo>

Needs approval:
- <yes/no and why>

Next command:
- <for example: $run-worker-goal <approved-goal>>
```
