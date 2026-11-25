---
name: sdlc-direct
version: 0.1.0
license: Apache-2.0
discoverable: true
authors: [agentic-os]
description: Lightest-ceremony entry point into the agentic-sdlc pipeline for a task the user has already judged small and unambiguous. Invoke on phrases like "just do this quickly", "small fix, skip the ceremony", "simple task, no spec needed", or "run sdlc-direct on <task>". Runs a mandatory research pass via the codebase-scout agent, a binary Clear/Unclear clarity check capped at 3 questions instead of complexity scoring or brainstorming, skips spec.md entirely, then proceeds through planning, QA checklist, inline TDD, QA test review, up to two code-review rounds, quality gates, and a QA health update, ending in a handoff message rather than an automatic merge or PR. Not for: ambiguous or ticket-sized work (sdlc-guided / sdlc-auto) or tasks the user already sized XS/S/M (sdlc-brief).
---

# sdlc-direct

## Shared contract preflight

Before workflow actions, send this JSON request to the installed plugin's
`runtime/run.py` using Python 3.10+ (resolve the plugin root on the current host):

```json
{"api_version":"1.0.0","operation":"policy.resolve","entrypoint":"sdlc-direct"}
```

Use the returned policy and `references/runtime-contracts.md` for contract identifiers,
limits and dependency floors. Unknown fields or incompatible versions block startup.
Task envelopes use `contract_version: "1.0.0"` and `task_input`; legacy `raw_input`
is accepted only by the explicit `input.normalize` compatibility adapter with `legacy: true`.
This preflight validates policy; durable lifecycle and host enforcement are separate
capabilities. Never infer those capabilities from a successful policy response.


Minimum-ceremony SDLC flow for work the user has already declared simple and clear. No spec
document, no complexity scoring, no brainstorming session — just a mandatory research pass, a
bounded clarity check, and straight into planning. Human-in-the-loop at every judgment gate,
always.

## When to invoke

Trigger on direct asks for the lightest flow: "just do this quickly," "small fix, skip the
ceremony," "simple task, no spec needed," "run sdlc-direct on <task>." Do not invoke when:

| Situation | Use instead |
|---|---|
| Ticket-sized, ambiguity expected, full audit trail | `sdlc-guided` |
| Ticket-sized, low-touch automation, audit trail | `sdlc-auto` |
| User pre-classified task size XS/S/M | `sdlc-brief` |
| Simple/clear, research-first, no spec | `sdlc-direct` (this skill) |

> If Stage 1 research turns up broad scope, or the task description contains risk keywords
> (`security`, `auth`, `migration`, `breaking`), print the relevant nudge below and proceed anyway
> — sdlc-direct never refuses, it only flags.

## Inputs

| Field | Type | Default | Notes |
|---|---|---|---|
| `task_description` | free text | — | required |
| `mode` | `main` \| `sync` | `main` | `sync` re-enters an existing maintenance-phase task |
| `slug` | string | kebab-case of `task_description`, truncated to 50 chars | task directory suffix |
| `ui` | boolean | `false` | gates whether `acceptance-check` can run at Stage 8 |

## Directory and state contract

Every run lives under a single task directory, no worktree, no `meta.json`:

```
docs/superpowers/tasks/YYYY-MM-DD-<slug>/
```

`YYYY-MM-DD` is the UTC date of the initial Stage 1 invocation. All reads and writes into this
tree go through the Read/Write/Edit tools — never shell redirection.

One state file per run, `<task-dir>/.state.json`. Initial write at Stage 1:

```json
{"schema": 1, "flow": "sdlc-direct", "slug": "<slug>", "branch": "<current branch>", "phase": "main", "started_at": "<ISO>"}
```

Full schema, including the fields Stage 10 and sync mode add:

```json
{
  "schema": 1,
  "flow": "sdlc-direct",
  "slug": "<slug>",
  "branch": "<current branch>",
  "phase": "main | maintenance",
  "started_at": "<when Stage 1 began, ISO>",
  "completed_at": "<written at Stage 10, ISO>",
  "last_sync_commit": "<the HEAD sha the last sync reconciled against>"
}
```

`flow` must always be the literal `"sdlc-direct"`. The `sdlc-stage-guard` hook reads this field to
select stage numbering; if it's absent, the hook falls back to `sdlc-brief` numbering and mislabels
every stage from here on. Never omit it, never let another skill overwrite it.

No `meta.json`, no `spec.md`, no `complexity-assessment.md`, no per-task `evidence/*.json` — those
belong to the heavier pipeline skills, not this one. Never read `.agents/memory/sdlc/` — that
store is reserved for the heavy pipeline.

## Artifacts under `<task-dir>`

| File | Written at | Producer |
|---|---|---|
| `technical-analysis.md` | Stage 1 | `codebase-scout` agent |
| `plan.md` | Stage 3 | `superpowers:writing-plans` |
| `qa-checklist.md` | Stage 4 (if not skipped) | `qa-scoping --checklist` |
| `qa-test-review.md` | Stage 6 (if not skipped) | `qa-scoping --review-tests` |
| `code-review.diff` | Stage 7 | `git diff` |
| `code-review-final.json` | Stage 7 | `code-review-orchestrator` |
| `code-review-check.diff` | Stage 7, fix-up only | `git diff` |
| `code-review-check.json` | Stage 7, fix-up only | `code-review-orchestrator` |
| `qa-report.md` | Stage 8 | `gate-runner` |
| `gate-plan.json` | Stage 8 | `gate-runner` |
| `acceptance-check-plan.json`, `evidence/verification/*.json` | Stage 8, `--ui` only | `acceptance-check` |
| `.state.json` | Stage 1 onward | this skill |

## Operating steps

### Stage 0 — Pre-flight

1. Confirm `superpowers:brainstorming` resolves at >= 6.1.0 and `git --version` succeeds. If
   either is unresolvable, print:
   ```
   sdlc-direct requires the superpowers plugin (>= 6.1.0).
   Install: /plugin marketplace add obra/superpowers && /plugin install superpowers
   ```
   and HALT.
2. Check `.agentic/agentic-sdlc/doctor.json` against the standard TTL + fingerprint rule (default
   7 days) — same mechanism `sdlc-brief` Stage 0 uses. Re-run the underlying checks only when the
   cache is stale or the fingerprint no longer matches.
3. Branch guard:
   - `git status --porcelain` dirty → HITL choice: `stash`, `commit first`, `hard reset` (requires
     explicit confirmation), `proceed with the existing dirty state` (warn first), or `abort`.
   - On a base branch → ask the user for a feature-branch name; read the base-branch config from
     `.agentic/guides/standards/git-workflow.md`; switch or create the branch only after
     confirming it's current with latest base.
   - Autonomous operation attempted while the tree is dirty or the branch decision is ambiguous →
     halt. This skill is HITL-only, unconditionally.

### Stage 1 — Research (hard gate)

Dispatch the `codebase-scout` agent whenever `<task-dir>/technical-analysis.md` is missing or
malformed. There is no exception for "simple task," "familiar codebase," or "prior context" — the
research pass always runs unless a valid file already exists.

A research file only counts as valid if it contains both literal section headers **Codebase
Findings** and **Risk Indicators**. Anything else — missing file, missing either header — forces a
fresh dispatch.

If `codebase-scout` reports **Research Blocked — Ticket Content Not Resolved**, surface the blocker
to the user and ask for the ticket description or acceptance criteria directly.

Write the initial `.state.json` (schema above) once research is underway.

> Risk Indicators listing 5+ items → print:
> `Research found broad scope — consider sdlc-guided or sdlc-auto. Proceeding with sdlc-direct.`
> Task description containing `security`, `auth`, `migration`, or `breaking` → print:
> `Heads-up: this task looks risky — consider sdlc-guided or sdlc-auto. Proceeding with sdlc-direct because that's what you asked for.`
> Neither nudge blocks progress — sdlc-direct proceeds regardless.

### Stage 2 — Clarity check

Binary verdict only: **Clear** or **Unclear**. This replaces complexity scoring and brainstorming
entirely — sdlc-direct never dispatches `sizing-analyst` and never opens a
`superpowers:brainstorming` session.

- **Clear** → go straight to Stage 3.
- **Unclear** → ask one targeted question, re-evaluate, repeat. Cap at 3 questions total. If still
  unclear at the cap, proceed anyway: log a `## Clarification assumptions` section at the top of
  `plan.md` recording what was assumed, and print:
  ```
  This task may benefit from full brainstorming — consider sdlc-brief instead. Proceeding with sdlc-direct.
  ```

### Stage 3 — Plan

Run `superpowers:writing-plans` directly against the research file — no spec.md, no `story-proxy`
involvement (there's nothing for it to stand in for; this flow has no requirements document).

Every implementation task line must carry a `Test-first: yes/no` annotation with a failing-test
description, e.g.:

```
- [ ] Add rate-limit header check — Test-first: yes — expect 429 after 6th request in 60s window
```

Route the drafted plan through `gate-arbiter` (`mode: "hitl"`) at gate `plan.approved`, with
`run_dir: <task-dir>` and bounded `ArtifactRefs` for the plan.

- `approve` → Stage 4.
- `request-changes` → feed follow-ups back into `superpowers:writing-plans`, rewrite `plan.md`,
  re-submit to the same gate.
- `abort` → stop the run.

### Stage 4 — QA checklist (conditional)

Skip entirely if `.agentic/guides/testing/qa-strategy.md` does not exist — QA foundation hasn't
been run for this repo. Log, verbatim:

```
QA knowledge foundation not found — skipping qa-scoping. Run the `qa-baseline` skill to enable QA-guided development.
```

Otherwise dispatch `qa-scoping --checklist`, writing `qa-checklist.md`. The `qa-checklist.approved`
gate is called by `qa-scoping` internally, not by this skill directly.

### Stage 5 — Implementation (inline, never subagent-dispatched)

Run `superpowers:test-driven-development` in the current conversation — never hand this off to a
subagent, and never substitute `superpowers:subagent-driven-development` here even though that
sub-skill exists as an option elsewhere in the ecosystem. Track one TodoWrite item per plan task.
RED and GREEN must both be visible in the transcript for every task marked `Test-first: yes`.

If a test does not fail before the implementation lands, stop and prompt the user (HITL, verbatim):

```
The test passed without implementation. Re-think the test or skip Test-first for this task?
```

`superpowers:test-driven-development` will eventually offer its own finishing/merge/PR/discard
menu (from `superpowers:finishing-a-development-branch`) — do not act on it. This flow owns
finishing: QA test review, code review, quality gates, then Stage 10 handoff. Ignore that menu
every time it surfaces mid-implementation.

### Stage 6 — QA test review (conditional)

Skipped under the same condition as Stage 4 (`qa-strategy.md` absent).

Otherwise run `qa-scoping --review-tests`, writing `qa-test-review.md`.

- `approve` → Stage 7.
- `request-changes` → fix high-severity findings inline, retry `qa-scoping --review-tests` exactly
  once. Still `request-changes` after that retry → escalate to the user. Never retry a second time.

### Stage 7 — Code review (at most two rounds)

Generate the review diff, excluding the lockfile:

```
git diff <merge_base>...HEAD -- . ':(exclude)package-lock.json' > <task-dir>/code-review.diff
```

Build the `ArtifactRefs` bundle — `kind`, `path`, `summary`, `signature` (sha-256) per entry, no
`spec` key ever (sdlc-direct has no spec.md); omit `qa-checklist` if Stage 4 was skipped:

```json
{
  "plan":         {"kind": "plan",         "path": "<task-dir>/plan.md",              "summary": "<2KB extract>", "signature": "<sha-256>"},
  "diff":         {"kind": "diff",         "path": "<task-dir>/code-review.diff",     "summary": "<diffstat + risk flags>", "signature": "<sha-256>"},
  "qa-checklist": {"kind": "qa-checklist", "path": "<task-dir>/qa-checklist.md",       "summary": "<N blocking scenarios>", "signature": "<sha-256>"}
}
```

Dispatch `code-review-orchestrator`, route its verdict through `gate-arbiter` at gate
`code-review.final`, writing `code-review-final.json`.

- **Safe-fail check first**: if the orchestrator's canonical verdict file shows empty `findings[]`
  and `confidence: "low"`, the review did not actually run. Repair the inputs (regenerate the diff,
  check `ArtifactRefs` paths) or escalate to the user. Never treat this as "no issues found," and
  never follow it with a check round.
- Classify the outcome by reading `code-review-final.json` directly — not the router's returned
  decision wrapper.
- `approve` → Stage 8.
- Real `request-changes` findings → capture the reviewed commit *before* touching anything:
  ```
  reviewed_head=$(git rev-parse HEAD)
  ```
  Fix inline, preserving finding IDs. Regenerate the fix-up diff against that captured commit:
  ```
  git diff "$reviewed_head" -- . ':(exclude)package-lock.json' > <task-dir>/code-review-check.diff
  ```
  Run exactly one check round at gate `code-review.check`, passing `prior_verdict` as the full
  `code-review-final.json` object (required — omitting it causes the orchestrator's check mode to
  safe-fail). Write `code-review-check.json`.
  - `approve` → Stage 8.
  - `request-changes` again → escalate to the user. No third automated round, ever, under any
    circumstance.

### Stage 8 — Quality gates

Run `gate-runner`, writing `qa-report.md` and `gate-plan.json`.

- `passed: true` → Stage 9.
- `passed: false` → print the blocked-gate detail, route through `gate-arbiter` at gate
  `feature.verification`, re-run `gate-runner`. Up to 3 retries total.

If `ui === true` **and** the diff touches a user-visible surface, dispatch `acceptance-check`,
writing `acceptance-check-plan.json` and `evidence/verification/*.json`. Skip it otherwise —
this is opt-in, never automatic.

### Stage 9 — QA health update (conditional)

Skip if Stage 4 was skipped, or if Stage 8 ever returned `passed: false` — health updates only
happen on green builds. Otherwise run `qa-scoping --update` against
`.agentic/guides/testing/qa-health.md`.

### Stage 10 — Handoff

Print a summary — no automatic merge, PR, or branch-discard action. This is the deliberate boundary
between this skill and `mr-submit`:

```
<slug> is ready on <branch>. What it left behind:
  <task-dir>/technical-analysis.md — what the codebase said
  <task-dir>/plan.md              — what was intended
  <task-dir>/qa-report.md         — what the gates found
Open the MR with `mr-submit`, or whatever you normally use.
```

Update `.state.json`: set `completed_at`, keep `phase: "main"` unless the user starts sync mode
afterward.

## Sync mode (`mode: "sync"`)

After Stage 10, a run can be re-entered in maintenance mode to reconcile `plan.md` against
post-completion commits.

- Entry check: if the matched task dir's `.state.json.phase !== "maintenance"`, print, verbatim:
  ```
  sync requires an existing task in maintenance mode; nothing to do.
  ```
- If multiple maintenance-phase task directories match, ask the user via `AskUserQuestion` which
  slug to sync.
- Compare current `HEAD` to `last_sync_commit` to detect plan/implementation drift.
- Present the unified diff via `AskUserQuestion` with options `apply | reject | request-edit`:
  - `apply` → update `last_sync_commit` to current `HEAD`, print
    `Plan synced through commit <sha>.`
  - `reject` → discard the proposed reconciliation.
  - `request-edit` → regenerate the proposal and re-prompt.
- Running sync twice in a row with no new commits is a no-op once `last_sync_commit === HEAD`.

To set `phase: "maintenance"` in the first place, this happens once, automatically, right after
Stage 10 completes on the initial `main`-mode run.

## Mid-run updates

If the user changes direction while a stage is in flight:

| Stage | User says | Action |
|---|---|---|
| 2 | Add a requirement | Append to the requirements block, re-run the clarity evaluation |
| 3 | Reorder or add a task | Edit `plan.md` directly |
| 5 | Change validator behavior | Edit the current plan task's body; redo completed tasks only if their behavior is invalidated |
| 7 | Reviewer finding | Fix inline; edit the plan only if it changes behavior |
| 8 | `gate-runner` fails | Fix inline; no artifact edit |

## Failure handling

| Failure | Response |
|---|---|
| `superpowers:writing-plans` aborts | Abort the run; keep `technical-analysis.md` for re-entry |
| TDD test won't fail | Stop, HITL prompt (verbatim text in Stage 5) |
| `code-review-orchestrator` returns malformed JSON | `gate-arbiter` HITL prompt showing the raw output |
| `code-review.check` still requests changes | Escalate; no auto-loop |
| `gate-runner` blocks on a missing runner | Follow `gate-runner`' own ask-once-then-cache flow |
| User Ctrl-C mid-stage | `.state.json` retains the current phase; re-running the same slug re-enters that stage from scratch |

## Config and guide paths this skill reads

| Path | Purpose |
|---|---|
| `.agentic/guides/standards/git-workflow.md` | Base-branch config for the Stage 0 branch guard |
| `.agentic/agentic-sdlc/doctor.json` | Stage 0 pre-flight cache |
| `.agentic/guides/testing/qa-strategy.md` | Presence check gating Stages 4/6/9 |
| `.agentic/guides/testing/qa-health.md` | Updated by Stage 9 |
| `.agents/memory/sdlc/` | Never read — reserved for the heavy pipeline |

sdlc-direct does not ship its own `references/` tree. Review methodology it relies on at Stage 7
lives in `code-review-orchestrator/references/review-lenses.md`, owned by that skill; treat it as
an upstream dependency rather than something this skill maintains. Any repo-level agent guidance
this skill's dispatched agents rely on comes from `repo-guides` / `repo-audit-guides`, not from a
bundled reference directory here.

## Gate ids (all called with `gate-arbiter`, `mode: "hitl"`)

| Gate id | Stage | Notes |
|---|---|---|
| `plan.approved` | 3 | — |
| `qa-checklist.approved` | 4 | called inside `qa-scoping`, not directly by this skill |
| `code-review.final` | 7 | — |
| `code-review.check` | 7 | only if changes were requested at `code-review.final`; requires `prior_verdict` |
| `feature.verification` | 8 | on `gate-runner` failure |

## Agents and skills this flow touches

`codebase-scout` (agent, Stage 1) · `superpowers:brainstorming` (presence check only — never run)
· `superpowers:writing-plans` (Stage 3) · `superpowers:test-driven-development` (Stage 5, inline)
· `superpowers:finishing-a-development-branch` (surfaced by TDD, explicitly not acted on) ·
`superpowers:subagent-driven-development` (mentioned as an alternative elsewhere in the ecosystem,
not used here) · `qa-scoping` (`--checklist`, `--review-tests`, `--update`) · `gate-runner` ·
`acceptance-check` · `gate-arbiter` · `code-review-orchestrator` · `mr-submit` (handoff
target only, never invoked automatically) · `sdlc-stage-guard` (hook, reads `.state.json.flow`).

Sibling entry points: `sdlc-brief`, `sdlc-guided`, `sdlc-auto`.

## Non-goals

- No complexity assessment, no `sizing-analyst` dispatch.
- No brainstorming session, no `spec.md`, no `story-proxy` involvement.
- No reading `.agents/memory/sdlc/`.
- No git worktree creation.
- No autonomous approval anywhere — HITL only, always.
- No per-task `evidence/*.json` files, no `meta.json`.
- No `acceptance-check` unless `ui: true` was passed in.
- No third automated code-review round, ever.
- No shelling out for file reads — Read/Write/Edit only.
- No automatic merge, PR, or branch-discard at the end of implementation. The TDD sub-skill's
  finishing menu is ignored until Stage 10, and Stage 10 itself only prints next-step guidance.
