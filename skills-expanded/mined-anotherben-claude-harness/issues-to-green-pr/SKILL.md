---
name: issues-to-green-pr
description: >
  Automation-safe GitHub issue to green PR orchestrator. Use when Codex is asked
  to process GitHub issues labeled bug or needs-triage, run a one-agent-one-job
  repair workflow, create or babysit PRs, get PR checks/review threads green,
  or run a recurring Codex automation that turns eligible issues into proved
  pull requests. Requires diagnose, blast-radius, patch-or-fix, structured JSON
  handoffs, Codex subagents for worker roles, builder self-review, independent
  review, live proof, and explicit authorization before merges or issue closure.
---

# Issues To Green PR

## Purpose

Drive eligible GitHub issues to reviewed, proved PRs without letting a single
agent blur discovery, implementation, review, proof, and shipping.

This is an orchestrator skill. The lead coordinates, verifies evidence, and
enforces stop rules. It does not let any worker mark its own work complete.

If the user asks to create, update, or run this on a schedule, use Codex's
automation tooling. Do not hand-roll a scheduler with shell loops. A manual
invocation runs one bounded tick.

## Non-Negotiables

- One Codex subagent gets one job. Separate intake, diagnosis, blast-radius,
  build, test/proof, self-review receipt, independent review, patch-or-fix, PR
  babysitting, and deployment proof.
- The lead orchestrates and verifies. The lead must not silently do worker-role
  work inline. If subagent dispatch is unavailable, stop the issue as `blocked`
  unless the user explicitly authorizes a degraded solo run for that issue.
- Every agent writes a JSON output file before handoff. Read
  `references/state-contract.md` before producing or consuming state files.
- Every agent includes a `self_review` block in its JSON output. Self-review is
  a receipt, not approval. The next agent performs the actual review.
- `$diagnose`, `$blast-radius`, and `$patch-or-fix` are mandatory gates for each
  issue that reaches code-change consideration.
- Do not build from issue prose alone. Issue text is intake, not proof.
- Do not use mock-only proof for runtime, schema, browser, worker, integration,
  or data-integrity behavior when live/local proof is available.
- Do not merge, close issues, mutate production, or run external write canaries
  unless the run config explicitly authorizes that exact action.
- If the current repo route card forbids editing, move build work into an
  allowed isolated worktree. Keep global automation state outside the guarded
  repo if needed.
- If a phase cannot be proved, stop with the issue state `blocked` or
  `needs-diagnosis`, not `green`.

## Subagent Dispatch Requirement

Use Codex subagents or separate Codex sessions for worker roles. The lead may
perform preflight, locking, live GitHub gate discovery, dispatch, integration,
and final status reporting. All phase work that creates or evaluates evidence
must be done by a distinct worker:

- intake subagent
- diagnosis subagent
- blast-radius subagent
- build subagent
- proof subagent
- independent-review subagent
- patch-or-fix subagent
- PR babysitter subagent
- deployment-proof subagent when merge mode is authorized
- issue-close subagent when close is authorized

Worker JSON must record `agent_instance_id` or `subagent_session_id`, role,
inputs, outputs, and self-review. The same subagent/session may not perform two
roles for the same issue, may not review its own output, and may not approve its
own proof. If a worker needs a different job, the lead opens a new subagent with
a new one-job prompt and passes only the required JSON/source pointers.

## Run Modes

- `green-pr` default: create or update a PR, make checks green, resolve review
  threads, prove behavior, and stop before merge.
- `merge-dev`: allowed only when the user or automation config explicitly says
  dev merges are authorized for this run.
- `merge-main`: allowed only when the user or automation config explicitly says
  main/prod promotion is authorized for this run.
- `audit-only`: inspect eligible issues, close none, mutate none, and output a
  categorized queue.

Record the selected mode in `run.json`. If no mode is stated, use `green-pr`.

## Eligibility

Fetch live GitHub issues from the configured repo. The default candidate set is
open issues with label `bug` or `needs-triage`.

Before dispatching diagnosis, an intake agent classifies each issue:

- `eligible`: discrete bug with a plausible code/proof surface.
- `already-fixed-needs-proof`: maybe fixed, but needs current branch/runtime
  proof before close or comment.
- `needs-diagnosis`: symptom is real but root cause is unknown.
- `not-autofixable`: epic, PRD, spec task, chore, ops-only item, security
  incident, concurrency/lock escalation, finance/payment authorization, schema
  migration, tenant/auth boundary, or external write risk.
- `blocked`: missing credentials, route/worktree guard, rate limit, unknown
  repo state, or unsafe automation scope.

Never auto-fix `not-autofixable` items. Produce a handoff instead.

## State And Locking

Use a run-scoped state directory:

```text
~/.codex/runs/issues-to-green-pr/<run-id>/
```

If a repo-approved worktree allows local artifacts, mirror issue packets under:

```text
.codex/issues-to-green-pr/<run-id>/
```

Use a lock file before processing so two automation ticks cannot stack. If a
lock exists and is fresh, exit with `skipped_existing_run` and do not start
agents. If the lock is stale, record why it is stale before taking over.

## Front-Loaded PR Gate Contract

Before opening or updating a PR, the lead must create
`issues/<issue>/pr-readiness.json` and prove the branch is shaped for the repo's
known CI and review gates. Do not use review feedback as the first place these
gaps are discovered.

Query GitHub directly at the start of every run for branch protection, rulesets,
required status checks, and active PR workflows. Record the response in
`pr-readiness.json`. Local workflow files are planning evidence; GitHub's live
settings are the enforcement source of truth.

For Helpdesk, classify gate surfaces this way unless the live GitHub response
says otherwise:

- PR body sections: `What changed`, `Regression check`, `Blast radius`,
  `Edge cases`, and `Conversations addressed`.
- GitHub branch-protection required checks: whatever GitHub currently returns
  for the target branch. As of the 2026-06-13 live check, both `dev` and `main`
  required `enterprise-delivery-gate`, `review-ai`, and `review-hard`.
- GitHub ruleset required checks: whatever the branch rules endpoint currently
  returns. As of the 2026-06-13 live check, both `dev` and `main` required
  `copilot-review-wait` through a ruleset.
- Active workflow checks: active workflows such as `preflight-dev` and
  `preflight-main` may run on PRs even when they are not branch-protection
  required. Treat a red active workflow as not green, and run the local
  equivalent before opening the PR when the repo profile requires it.

If local scripts treat a check as advisory but GitHub branch protection or a
ruleset requires it, the live GitHub setting wins for that run.

The PR body must be evidence-bearing before PR creation. Generated placeholders
from `codex-pr-create` or `scripts/pr/create-enterprise-pr-body.cjs` are not
acceptable for `pr-open` or `pr-green`. Record exact command results and
PASS/FAIL status in the body:

- `Regression check`: focused tests, integration/live proof, target SHA, and
  `npm run local:canary` when opening or updating a PR to `dev` in a local
  linked-dev Helpdesk checkout.
- `Blast radius`: path to the blast-radius report/checklist, verdict, high or
  critical finding count, and why remaining findings are non-blocking.
- `Edge cases`: concrete falsification cases for null, empty, malformed,
  concurrent, boundary, tenant/auth/schema, and domain-specific behavior.
- `Conversations addressed`: `None yet` is acceptable only for a new PR before
  review has arrived. Updating an existing PR must list every actionable review
  thread or finding and the evidence-backed response.

Because no GitHub PR event payload exists before the PR is opened, validate the
body file directly before calling the wrapper. Confirm all required headings are
present and each section passes the same non-placeholder standard enforced by
`enterprise-delivery-gate`.

Run or justify the local equivalent of the repo gates before creating the PR:

```bash
node scripts/enterprise-delivery-gate.cjs --base origin/<base> --head HEAD --event pull_request
node scripts/ci/run-preflight.cjs --target <dev|main> --mode ci --base origin/<base> --head HEAD --event pull_request
node scripts/review/local-review.cjs --base origin/<base> --head HEAD --live-db required
```

Add these when the diff requires them:

```bash
GITHUB_BASE_REF=<base> node scripts/ci/ensureNoNewMockTests.cjs
node scripts/db-write-enforcement.cjs --base origin/<base> --head HEAD --event pull_request
node scripts/review/pr-readiness-substance-check.cjs --base origin/<base> --head HEAD
npm run local:canary
```

If `local-review` reports a required live-proof registry gap, do not open the
PR as green. Add the missing approved live-proof lane, run it, and record the
result first. If the branch is stale versus the target base, rebase or
linearize before PR creation and rerun affected proof.

Use the repo wrapper for PR creation:

```bash
/Users/ben/.codex/bin/codex-pr-create --base <dev|main> --title "<title>" --body-file <body.md>
```

Never rely on the wrapper's generated body for this skill. It is a fallback
scaffold, not a gate-complete delivery artifact.

## Workflow

### 1. Preflight

The lead does this directly:

- Read repo route/worktree guard and current git state.
- Confirm GitHub auth, repo name, default base branch, and target branch.
- Confirm automation mode and whether merge/close actions are authorized.
- Confirm local proof services and DB target if code may run.
- Create `run.json` and one `issues/<issue>/issue-intake.json` per candidate.

Stop before mutating if route, auth, branch, or runtime target is unsafe.

### 2. Intake Agent

One agent classifies one issue. It may inspect the live issue, linked PRs,
labels, recent comments, and current branch containment. It must write
`issue-intake.json`.

The intake agent must not edit code, close issues, create branches, or diagnose
root cause beyond classifying the queue.

### 3. Diagnose Gate

For every issue that is not closed by proven current evidence, dispatch one
diagnosis agent to run `$diagnose`.

Required outputs:

- canonical human-readable diagnosis rundown
- validated `diagnose.build_packet.v1`
- root cause status
- exact proof surface
- exact build boundaries or a stop reason

If `$diagnose` does not produce a valid packet or root-cause-ready handoff, stop
the issue. Do not build from partial diagnosis.

### 4. Blast-Radius Gate

Dispatch a separate blast-radius agent to run `$blast-radius` against the
diagnosis packet, planned change set, or current PR diff.

The agent must produce the markdown report/checklist required by the skill plus
`blast-radius-summary.json` with verdict, findings by severity, live schema
status, review-thread status, and required verification commands.

Any HIGH or CRITICAL blast-radius finding blocks build or merge until recycled.

### 5. Build

Only build when diagnose and blast-radius allow it. Create an isolated worktree
or use an allowed existing one.

Dispatch build agents with a single bounded job:

- one issue
- one owner boundary or file group
- exact allowed paths
- exact forbidden paths
- exact input JSON files
- exact output JSON path

Builders must implement the smallest root-cause fix, write tests or guards, run
their focused proof when available, and write `build-output.json` with a
`self_review` section. Builders must not approve, merge, close, or mark the
issue green.

### 6. Test And Runtime Proof

Dispatch a separate proof agent. It must run the commands named by diagnose,
blast-radius, and the build output, plus any live/browser/schema canaries needed
for the runtime surface.

Proof output must include command, environment, SHA, target service/database,
exit code, and relevant output snippets. Missing proof is a block.

### 7. Independent Review

Dispatch an independent reviewer after builder self-review exists. The reviewer
must read the builder output, self-review, diff, tests, and proof, then write
`independent-review.json`.

The reviewer must not edit code. If the reviewer finds a fixable issue, recycle
once to a new build agent with a new one-job prompt. Do not ask the same agent
to redo the same job unless inputs changed.

### 8. Patch-Or-Fix Gate

Dispatch a separate reviewer to run `$patch-or-fix` after independent review and
proof. This gate decides whether the change is a real fix, partial fix, patch,
or unproven.

Only `FIX` with required proof can proceed to PR-green work. Other verdicts
either recycle once with exact required fix instructions or stop with a handoff.

### 9. PR Green Work

Create PRs with the repo-approved wrapper when one exists. For Helpdesk, use
`/Users/ben/.codex/bin/codex-pr-create`, not plain `gh pr create`.

PR work requires `pr-readiness.json` to be complete before PR creation or PR
update. The lead must reject the PR step with `pr-not-ready` if the body,
local-gate evidence, live-proof lane, blast-radius verdict, or target-base
freshness is missing.

PR-green work then requires:

- PR body with required delivery sections and non-placeholder evidence.
- Current head SHA recorded in `pr.json`.
- Checks green on the current head.
- Codex review present for the current head when the repo requires it.
- Review threads resolved, using GraphQL thread state as the source of truth.
- `copilot-review-wait` or the repo's equivalent async review gate when present.
- Fresh blast-radius or review rerun if the head SHA changes materially.
- Runtime proof still current after rebase, force-push, or review-fix commits.

If the branch falls behind, rebase or linearize according to repo policy and
rerun affected proof. Never claim green from an older SHA.

### 10. Merge, Deploy, Close

Default mode stops at a green PR.

If the run mode authorizes merge:

- Run the repo's required pre-merge review wait command.
- Confirm required checks and review threads on the current head.
- Merge only with the allowed strategy for that branch.
- Run post-merge/dev/prod proof required by the repo.
- Close the GitHub issue only after the fix is merged to the authorized target
  and the closing proof is recorded in `issue-close.json`.

If close proof is dev-only and the issue describes production behavior, do not
close unless the run config says dev closure is acceptable.

## Agent Prompt Template

Every worker prompt must include:

```text
Role: <one role only>
Issue: <number and title>
Job: <one concrete job>
Inputs: <JSON paths and source pointers>
Allowed paths: <exact files/directories or read-only>
Forbidden: <actions and paths>
Required output: <JSON path and schema>
Stop rules: <conditions that must stop work>
Self-review: required before handoff
```

The lead rejects any worker output that lacks JSON, self-review, evidence
status, or a clear next-state recommendation.

## Finite Loop

For each issue:

- One initial diagnose/blast/build/proof/review/patch-or-fix pass.
- One recycle pass if the blocker is exact and bounded.
- Stop after the same blocker repeats, after unsafe scope expansion, or after
  the issue changes class.

Never hide an unresolved blocker by opening a weaker PR.

## Completion States

Use these exact issue states in JSON:

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

Final response should report counts by state, PR links, blocked reasons, and
the next safest action. Keep it concise; the JSON files carry the detail.
