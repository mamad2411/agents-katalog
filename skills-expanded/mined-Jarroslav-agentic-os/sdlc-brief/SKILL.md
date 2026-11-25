---
name: sdlc-brief
description: >
  Runs a lightweight, human-in-the-loop SDLC flow for a task the user has already
  sized as XS/S/M: brainstorm-lite, spec, plan, inline TDD, one code-review round,
  and gate-runner on the current feature branch — no complexity scoring, no per-task
  subagents, no evidence files, no worktrees. Invoke on phrases like "run sdlc-brief",
  "small task, just spec and build it", "quick fix workflow", "this is an XS/S/M
  task", "lightweight SDLC for this change", or a request to reconcile a finished
  task's spec/plan against changes made after handoff ("sdlc-brief sync", "sync my
  task", "reconcile the spec with what shipped", mode: sync). Not for: ambiguous or
  ticket-sized work that needs a full audit trail (sdlc-guided), low-touch
  full-pipeline automation (sdlc-auto), or simple research-first work with
  no spec (sdlc-direct).
version: 0.1.0
license: Apache-2.0
discoverable: true
author: agentic-os
---

# sdlc-brief

## Shared contract preflight

Before workflow actions, send this JSON request to the installed plugin's
`runtime/run.py` using Python 3.10+ (resolve the plugin root on the current host):

```json
{"api_version":"1.0.0","operation":"policy.resolve","entrypoint":"sdlc-brief"}
```

Use the returned policy and `references/runtime-contracts.md` for contract identifiers,
limits and dependency floors. Unknown fields or incompatible versions block startup.
Task envelopes use `contract_version: "1.0.0"` and `task_input`; legacy `raw_input`
is accepted only by the explicit `input.normalize` compatibility adapter with `legacy: true`.
This preflight validates policy; durable lifecycle and host enforcement are separate
capabilities. Never infer those capabilities from a successful policy response.


Lightweight orchestrator for tasks a human has already sized as XS/S/M. Picking this
skill **is** the complexity classification — there is no classifier inside it.
Everything runs inline, in the current conversation, on the current feature branch.

> Cost tradeoff: the full pipeline (`sdlc-engine`, invoked via `sdlc-guided` /
> `sdlc-auto`) buys audit depth with subagents-per-plan-task, an evidence
> trail, and worktree isolation. `sdlc-brief` spends none of that budget. If a task
> turns out to need it mid-flow, stop and hand it back rather than bolting the
> heavy machinery on partway through.

## Entry points into the parent plugin

| Use case | Entry point |
|---|---|
| Ticket-sized, ambiguity expected, full audit trail | `sdlc-guided` |
| Ticket-sized, low-touch automation, audit trail | `sdlc-auto` |
| Pre-classified XS/S/M, minimum ceremony | **`sdlc-brief`** (this skill) |
| Simple/clear, research-first, no spec | `sdlc-direct` |

## When the project owns implementation

Before any implementation, read `.agentic/agentic-sdlc/config.json` if it is there. Where it declares project
orchestrators, this skill owns intake, research, spec, plan, review and QA —
and nothing that writes code. Route the code-writing to the selected project
orchestrator and consume only its summary and gate results. Do not invoke the
project's fleet workers yourself, and do not open a competing orchestration state
file; the project's own is authoritative for the work it is running.

## Non-goals

- No effort-sizing step of its own — `sizing-analyst` only returns a routing
  verdict, never a gate.
- No `meta.json`, no per-phase status slots.
- No run ledger beyond the optional `decisions.jsonl` / `events.jsonl` that
  `gate-arbiter` writes on its own.
- No git worktrees under any host.
- No load of the heavy-pipeline memory directory (`.agents/memory/sdlc/`) — never
  read by this skill, in any stage, in any mode.
- No autonomous or stand-in approval at any judgment gate — HITL only, always.
- No per-task `evidence/*.json` — the conversation transcript is the record.
- No feature verification unless the `ui` input is explicitly `true`.

## Inputs

| Input | Type | Default |
|---|---|---|
| `task_description` | free text | — |
| `mode` | `main` \| `sync` | `main` |
| `slug` | string | kebab-case of `task_description`, truncated to 50 chars |
| `ui` | boolean | `false` |

## Task state

**Task directory:** `docs/superpowers/tasks/YYYY-MM-DD-<slug>/` — date is the UTC
date of the initial Stage 1 invocation, fixed for the life of the task.

**State file** `<task-dir>/.state.json` is the only tracking file this skill owns:

```json
{
  "schema": 1,
  "slug": "<slug>",
  "branch": "<current branch>",
  "phase": "main | maintenance",
  "started_at": "<when Stage 1 began, ISO>",
  "completed_at": "<written at Stage 11, ISO>",
  "last_sync_commit": "<the HEAD sha the last sync reconciled against>"
}
```

`phase` starts at `"main"` and flips to `"maintenance"` at Stage 11 handoff. From
that point, further code changes against the task are reconciled back into
`spec.md` / `plan.md` only through `mode: "sync"` — see below.

**Artifacts under `<task-dir>`:** `technical-analysis.md`, `complexity-assessment.md`,
`spec.md`, `plan.md`, `qa-checklist.md`, `qa-test-review.md`, `.state.json`,
`qa-report.md`, `gate-plan.json`, plus optional `decisions.jsonl` / `events.jsonl`
(owned by `gate-arbiter`), and — only if `ui` was on —
`acceptance-check-plan.json` and `evidence/verification/*.json`.

## References

This skill carries no bundled `references/` tree — it is a single-file orchestrator.
In place of static references it reads live repo state at each stage:

| Path | Read for |
|---|---|
| `.agentic/agentic-sdlc/doctor.json` | TTL+fingerprint cache (7-day default), same rule as `sdlc-engine` Phase 0 — re-verify environment (superpowers version, git availability) only when the fingerprint or TTL has expired |
| `.agentic/guides/standards/git-workflow.md` | configured base branch, branch/commit conventions |
| `.agentic/guides/testing/qa-strategy.md` | presence gates Stages 5, 7, 10 — absence skips all three |
| `.agentic/guides/testing/qa-health.md` | updated by Stage 10 |
| `.agents/memory/sdlc/` | **never read** — heavy-pipeline memory, out of scope here |

## Pre-flight (Stage 0)

1. Verify the host has the `superpowers` plugin at `>= 6.1.0`. If not, stop and
   print:
   > `sdlc-brief requires the superpowers plugin (>= 6.1.0).`
   > `Install: /plugin marketplace add obra/superpowers && /plugin install superpowers`
2. Load or refresh `.agentic/agentic-sdlc/doctor.json` per its TTL/fingerprint rule.
3. Risk-keyword heuristic: if `task_description` pairs an external ticket id with
   a term like security, auth, migration, or breaking, print:
   > `Heads-up: this task looks like it might need sdlc-guided. Proceeding with sdlc-brief because that's what you asked for.`
   and continue — never refuse.
4. Working-tree check (`git status --porcelain`). If dirty, offer exactly:
   stash / commit first / hard reset (only after explicit confirmation naming the
   branch) / proceed with dirty state (with a warning) / abort.
5. Branch check (`git branch --show-current`):
   - On the configured base branch: refresh (fetch, fast-forward only) if
     network/policy allow, verify clean, then create a feature branch; otherwise
     ask the user for a feature-branch name.
   - If the requested target branch already exists: reuse it if clean; otherwise
     require an explicit user choice among continue / recreate / reconcile / abort.

Blast radius: R0 (read-only) through this stage — no repo writes yet.

## Stage flow (1–11, inline in the current conversation)

| Stage | What happens | Blast radius |
|---|---|---|
| 1 | Dispatch `codebase-scout` (inputs `task_context`, `feature_area`, `run_dir`) → writes `technical-analysis.md`. May return "Research Blocked — Ticket Content Not Resolved". | R1 |
| 2 | Dispatch `sizing-analyst` (inputs `task_description`, `feature_area`, `run_dir`) → writes `complexity-assessment.md`. A `SPLIT REQUIRED` verdict halts the flow — hand decomposed stories back to the user before any brainstorming. | R1 |
| 3 | `superpowers:brainstorming` (brainstorm-lite) → `spec.md`. Gate **`spec.approved`** via `gate-arbiter`. | R1 |
| 4 | `superpowers:writing-plans` → `plan.md`. Gate **`plan.approved`**. Every plan task line must read `Test-first: yes/no — <failing test description>` (same contract `sdlc-engine` Phase 5 enforces). | R1 |
| 5 | `qa-scoping --checklist` (args `mode`, `run_dir`, `merge_base`) → `qa-checklist.md`. Gate **`qa-checklist.approved`** (called inside `qa-scoping`). **Skipped** if `qa-strategy.md` is absent. | R1 |
| 6 | `superpowers:test-driven-development`, inline — no per-task subagent. One `TodoWrite` item per plan task, transitioned `in_progress` → `completed` as each is finished. If a test passes before implementation exists, stop and ask: `The test passed without implementation. Re-think the test or skip Test-first for this task?` | R2 |
| 7 | `qa-scoping --review-tests` → `qa-test-review.md`. **Skipped** if `qa-strategy.md` is absent. A request-changes verdict gets exactly one retry after inline fixes, then escalates to the user — never a second automated pass. | R1/R2 |
| 8 | Code review. Gate **`code-review.final`** with the ArtifactRef bundle below. If it requests changes, fix inline (no artifact edit unless behavior changes) and re-gate at **`code-review.check`** — at most once. Still requesting changes after that escalates to the user; there is no third round. | R1/R2 |
| 9 | `gate-runner` (args `branch`, `merge_base` — default `origin/main` if unset — `repo_path`, `run_dir`) → `qa-report.md`, `gate-plan.json`. On failure, retry up to 3 times with user-selected fixes; after 3, escalate: `gate-runner blocked after 3 fix attempts; review needed.` Gate **`feature.verification`** fires on a `gate-runner` failure. If `ui` is `true` and the diff touches a UI surface named in `gate-plan.json`'s `ui_globs`, dispatch `acceptance-check` → `acceptance-check-plan.json`, `evidence/verification/*.json`. | R1/R2 |
| 10 | `qa-scoping --update` → updates `qa-health.md`. **Skipped** if `qa-strategy.md` is absent. | R1 |
| 11 | Handoff. Set `.state.json.phase = "maintenance"`, `completed_at`. Print the handoff block below and suggest `mr-submit`. | R1 |

Stages 5, 7, and 10 share one presence gate: no `.agentic/guides/testing/qa-strategy.md`
means all three are skipped, with:
> `QA knowledge foundation not found — skipping qa-scoping. Run the` `qa-baseline` `skill to enable QA-guided development.`

> Judgment gates routed through `gate-arbiter` always run in `mode: "hitl"` here
> — never autonomous fast-path, never deterministic auto-approval, never a
> subagent standing in for the user. A real user verdict is the only thing that
> resolves a gate.

## Gate ids routed through `gate-arbiter`

All calls use `mode: "hitl"`, `run_dir: <task-dir>`, and a bounded ArtifactRef
bundle.

| Gate id | Stage |
|---|---|
| `spec.approved` | 3, after `spec.md` written |
| `plan.approved` | 4, after `plan.md` written |
| `qa-checklist.approved` | 5, called inside `qa-scoping` |
| `code-review.final` | 8 |
| `code-review.check` | 8, only if `code-review.final` requested changes |
| `feature.verification` | 9, on a `gate-runner` failure |

**ArtifactRef shape** (Stage 8 example — `qa-checklist` entry omitted if Stage 5
was skipped):

```json
{
  "spec":         {"kind": "spec", "path": "<task-dir>/spec.md", "summary": "<2KB extract>", "signature": "<sha-256>"},
  "plan":         {"kind": "plan", "path": "<task-dir>/plan.md", "summary": "<2KB extract>", "signature": "<sha-256>"},
  "diff":         {"kind": "diff", "path": "<git diff <base>...HEAD output>", "summary": "<diffstat + risk flags>", "signature": "<sha-256>"},
  "qa-checklist": {"kind": "qa-checklist", "path": "<task-dir>/qa-checklist.md", "summary": "<N blocking scenarios>", "signature": "<sha-256>"}
}
```

## Agents and skills this orchestrator calls

**Agents:**

| Agent | Stage | Inputs | Writes |
|---|---|---|---|
| `codebase-scout` | 1 | `task_context`, `feature_area`, `run_dir` | `technical-analysis.md` |
| `sizing-analyst` | 2 | `task_description`, `feature_area`, `run_dir` | `complexity-assessment.md` |

**Skills:**

- `superpowers:brainstorming` — Stage 3
- `superpowers:writing-plans` — Stage 4
- `superpowers:test-driven-development` — Stage 6, inline, no subagent
- `qa-scoping` — modes `--checklist` (5), `--review-tests` (7), `--update` (10)
- `gate-runner` — Stage 9
- `acceptance-check` — Stage 9, conditional
- `gate-arbiter` — every gate above
- `mr-submit` — suggested at handoff, not auto-invoked
- `superpowers:writing-clearly-and-concisely` — optional, sync-mode prose cleanup only

> Contrast: `superpowers:subagent-driven-development` is what the full pipeline
> uses to fan work out per plan task. `sdlc-brief` deliberately does not use it —
> Stage 6 stays inline in this conversation, which is the whole point of the
> cost tradeoff.

## Git commands used

`git branch --show-current`, `git status --porcelain`, `git diff <base>...HEAD`.

## Handoff (Stage 11) — verbatim strings

```
Task <slug> ready on branch <branch>.
Spec: <task-dir>/spec.md
Plan: <task-dir>/plan.md
QA report: <task-dir>/qa-report.md
Invoke mr-submit (or your preferred PR tool) when ready.
```

## Sync mode (`mode: "sync"`)

Reconciles `spec.md` / `plan.md` against code changes made after Stage 11 handoff.
Not stage-numbered — it's a short, separate flow:

1. Require `<task-dir>/.state.json.phase === "maintenance"`. If no task is in that
   phase:
   > `sync requires an existing task in maintenance mode; nothing to do.`
2. If more than one task directory is in `maintenance` phase, ask via
   `AskUserQuestion` which slug to sync.
3. Idempotency: if `last_sync_commit === HEAD`, no-op — nothing to reconcile.
4. Diff the current tree against `last_sync_commit` (or `started_at`'s base if
   never synced), and for each drifted section present the user an
   `AskUserQuestion` with exactly `apply | reject | request-edit`.
5. Optionally invoke `superpowers:writing-clearly-and-concisely` to tidy prose
   in edited sections.
6. On completion, update `last_sync_commit` to `HEAD` and print:
   > `Artifacts synced through commit <sha>.`

Other tooling in the plugin (e.g. review or PR-creation flows detecting the
task's spec/plan no longer match the implementation) nudges the user back here
with:
> `spec/plan drifted from impl - invoke sdlc-brief with mode: "sync" before PR`

## Phase-aware edit rule

Editing `spec.md` from a later phase always requires user confirmation first.
Editing `plan.md` during planning does not require touching `spec.md` unless the
change implies a new requirement.

| Stage | User asks for | Skill does |
|---|---|---|
| 3 | Add scope | Edit `spec.md`, re-run the brainstorm step |
| 4 | Reorder/add a task | Edit `plan.md` only |
| 4 | New requirement | Edit `plan.md` + `spec.md` (confirm first) |
| 6 | Change behavior | Edit `plan.md`; redo only the completed tasks it invalidates |
| 8 | Review finding | Fix inline; no artifact edit unless behavior changes |
| 9 | `gate-runner` failure | Fix inline; no artifact edit |

## Failure handling

| Situation | Outcome |
|---|---|
| Brainstorming aborted | Skill aborts, no files written |
| Plan-writing aborted | Skill aborts, `spec.md` persists for re-entry |
| TDD test refuses to fail | Stop, HITL prompt (see Stage 6) |
| Malformed JSON from a helper | `gate-arbiter` HITL prompt with the raw output shown |
| `code-review.check` still requests changes | Escalate to the user — no third round |
| `gate-runner` blocked on a missing runner | Defer to `gate-runner`'s own ask-once-then-cache flow |
| Ctrl-C mid-stage | `.state.json` retains its phase; re-run re-enters that stage from scratch |

## Model tiers

Judgment-heavy stages — brainstorm-lite, planning, code review — justify
standard/premium tier. Deterministic stages — pre-flight checks, `gate-runner`
runner detection — are economy-tier work; don't over-provision them.

## Cross-references

- Shares the TTL/fingerprint doctor-check and the `Test-first:` plan-line contract
  with `sdlc-engine` (the full/heavy orchestrator).
- Depends on but does not redefine: `superpowers` (floor `>= 6.1.0`), `qa-baseline`
  (upstream prerequisite for Stages 5/7/10), `gate-arbiter`, `qa-scoping`,
  `gate-runner`, `acceptance-check`, `mr-submit`.
- After `mr-submit` opens the PR, hand off to `mr-watch` if the user wants it
  monitored to merge — that's a separate, explicit invocation, not something this
  skill triggers on its own.
