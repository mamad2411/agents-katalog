---
name: issue-to-green-pr
description: >
  Standalone single GitHub issue to green PR orchestrator. Use when Codex is
  asked to target one specific GitHub issue number, owner/repo#number, or issue
  URL and drive it through a one-subagent-one-job repair workflow into a proved
  PR. Requires diagnose, blast-radius, patch-or-fix, live GitHub gate discovery,
  structured JSON handoffs, Codex subagents for worker roles, independent
  review, front-loaded PR readiness, and explicit authorization before merge or
  issue closure.
---

# Issue To Green PR

## Purpose

Drive exactly one targeted GitHub issue to a reviewed, proved PR. This is the
standalone form of the issue-to-green workflow: no queue sweep, no label scan,
and no opportunistic adjacent issue processing.

The lead orchestrates, verifies handoffs, and reports status. Worker phase work
must be done by distinct Codex subagents or separate Codex sessions.

## Target Requirement

Require one explicit target:

```text
https://github.com/<owner>/<repo>/issues/<number>
<owner>/<repo>#<number>
#<number> in the current repo
```

If only an issue number is supplied, resolve the repo from the local git remote.
If the repo is ambiguous, stop and ask for the repo. Do not fetch or process any
other issue unless the user explicitly retargets the run.

An explicit target may bypass the batch skill's label eligibility filter, but
not the safety gates. If the issue is an epic, vague feature request, security
incident, schema/auth/tenant/payment risk, external-write risk, or lacks a
provable bug surface, stop with a handoff instead of forcing a PR.

## State

Read `references/state-contract.md` before writing or consuming run JSON.

Default state directory:

```text
~/.codex/runs/issue-to-green-pr/<run-id>/issues/<issue-number>/
```

Use a per-issue lock. If a fresh lock exists for the same repo and issue, exit
with `skipped_existing_run`.

## Run Modes

- `green-pr` default: produce or update a PR, get it green, and stop before
  merge.
- `audit-only`: inspect the single issue and write a handoff; mutate nothing.
- `merge-dev`: only when explicitly authorized for this run.
- `merge-main`: only when explicitly authorized for this run.

No mode may close the issue unless closure is explicitly authorized and merged
proof exists for the authorized target.

## Mandatory Gates

For every targeted issue that reaches code-change consideration:

- run `$diagnose`
- run `$blast-radius`
- run `$patch-or-fix`
- run live GitHub branch-protection/ruleset/workflow discovery before PR work
- run repo-local pre-PR readiness gates before creating or updating the PR
- run independent review after builder self-review and before patch-or-fix

Missing proof is a blocker. Do not claim green from issue prose, stale CI, a
worker summary, or a previous SHA.

## Subagent Rules

One Codex subagent gets one job. Required roles for a full fix lane:

- `intake-agent`
- `diagnosis-agent`
- `blast-radius-agent`
- `build-agent`
- `proof-agent`
- `independent-review-agent`
- `patch-or-fix-agent`
- `pr-babysitter-agent`
- `deployment-proof-agent` only in authorized merge modes
- `issue-close-agent` only when closure is authorized

The same subagent/session may not perform two roles for the same issue, review
its own output, or approve its own proof. If subagent dispatch is unavailable,
stop as `blocked` unless the user explicitly authorizes degraded solo mode.

Every worker writes JSON with `agent_instance_id` or `subagent_session_id`,
inputs, outputs, evidence, blockers, and `self_review`.

## Workflow

### 1. Resolve Target

The lead resolves repo, issue number, issue URL, base branch, current branch,
route/worktree guard, GitHub auth, and run mode. It writes `run.json` and
`target-issue.json`.

Stop before mutation if the target issue, repo, auth, route, branch, or runtime
proof surface is unsafe.

### 2. Intake

Dispatch an intake subagent for the one target issue. It fetches live issue
state, labels, linked PRs, recent comments, and current branch containment. It
classifies the target as `eligible`, `already-fixed-needs-proof`,
`needs-diagnosis`, `not-autofixable`, or `blocked`.

The intake subagent must not edit code, create branches, or close the issue.

### 3. Diagnose

Dispatch a diagnosis subagent to run `$diagnose`. Require a valid
`diagnose.build_packet.v1`, root-cause status, proof surface, allowed build
paths, and stop reason when root cause is not ready.

Do not build from partial diagnosis.

### 4. Blast Radius

Dispatch a separate blast-radius subagent to run `$blast-radius` against the
diagnosis packet and planned change set. HIGH or CRITICAL findings block build
or PR work until recycled.

### 5. Build

Dispatch one build subagent for the smallest root-cause fix. Give it one issue,
one owner boundary or file group, exact allowed paths, exact forbidden paths,
and exact output path. The builder writes tests or guards, runs focused feedback
commands, and records self-review.

The builder cannot approve, prove, merge, close, or mark the issue green.

### 6. Proof

Dispatch a proof subagent. It runs the commands named by diagnose,
blast-radius, and build output, plus live/browser/schema canaries required by
the runtime surface. It records command, environment, SHA, target DB/service,
exit code, and snippets.

### 7. Independent Review

Dispatch an independent-review subagent after builder self-review exists. It
reviews diff, tests, proof, build output, and self-review. It does not edit
code. Fixable findings recycle once to a new build subagent with a new one-job
prompt.

### 8. Patch Or Fix

Dispatch a separate reviewer to run `$patch-or-fix`. Only `FIX` with required
proof can proceed to PR work. `PATCH`, partial, or unproven verdicts either
recycle once with exact instructions or stop with a handoff.

### 9. Front-Loaded PR Readiness

Before opening or updating a PR, create `pr-readiness.json`.

For Helpdesk-style repos, query GitHub directly for branch protection, branch
rules/rulesets, required status checks, active workflows, and review-thread
requirements. GitHub live settings override local assumptions.

Prepare a PR body with non-placeholder evidence for:

- `What changed`
- `Regression check`
- `Blast radius`
- `Edge cases`
- `Conversations addressed`

Run or justify local equivalents such as:

```bash
node scripts/enterprise-delivery-gate.cjs --base origin/<base> --head HEAD --event pull_request
node scripts/ci/run-preflight.cjs --target <dev|main> --mode ci --base origin/<base> --head HEAD --event pull_request
node scripts/review/local-review.cjs --base origin/<base> --head HEAD --live-db required
node scripts/review/pr-readiness-substance-check.cjs --base origin/<base> --head HEAD
npm run local:canary
```

Use the repo wrapper when present. For Helpdesk:

```bash
/Users/ben/.codex/bin/codex-pr-create --base <dev|main> --title "<title>" --body-file <body.md>
```

Never rely on generated wrapper placeholder text as readiness evidence.

### 10. PR Green

Dispatch a PR babysitter subagent. It tracks current head SHA, check runs,
review decisions, review threads, async review gates, and stale-base state. If
the branch rebases or receives review-fix commits, rerun affected proof and
refresh `pr-readiness.json`.

Default completion is `pr-green`, not merge.

### 11. Merge And Close

Only in an authorized merge mode:

- run the repo's pre-merge review wait command
- confirm required checks and review threads on the current SHA
- merge using the allowed strategy
- dispatch deployment-proof subagent for post-merge/dev/prod proof
- close the GitHub issue only after the authorized target and close proof are
  recorded in `issue-close.json`

## Agent Prompt Template

```text
Role: <one role only>
Issue: <owner>/<repo>#<number> and title>
Job: <one concrete job>
Inputs: <JSON paths and source pointers>
Allowed paths: <exact files/directories or read-only>
Forbidden: <actions and paths>
Required output: <JSON path and schema>
Stop rules: <conditions that must stop work>
Self-review: required before handoff
```

The lead rejects output missing JSON, worker identity, self-review, evidence
status, or a clear next-state recommendation.

## Completion States

Use only these states:

- `skipped_existing_run`
- `not-autofixable`
- `blocked`
- `needs-diagnosis`
- `diagnosed`
- `build-ready`
- `built-pending-proof`
- `proof-failed`
- `review-failed`
- `patch-not-fix`
- `pr-not-ready`
- `pr-open`
- `pr-green`
- `merged-pending-proof`
- `closed-proven`

Final output should name the single issue, state, PR URL if any, blocking
reason if any, and next safest action.
