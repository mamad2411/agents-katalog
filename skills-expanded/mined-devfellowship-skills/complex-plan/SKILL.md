---
name: complex-plan
description: "Use BEFORE writing a plan for large software work — a new app, a redesign, a mobile version, a cross-service pipeline or integration, anything that will become 3+ PRs or be executed by other agents. Routes through the pack in a fixed order (ground truth → two-planner draft → acceptance gates → PR slicing → readiness review → execution handoff), names the file each phase produces and the hard gates a plan must pass before it is published. Skip for a one-file bug fix, a question, or a small edit to a plan that already exists."
author: SamuelStefano
tags: [planning, architecture, multi-agent, pack]
---

# Complex plans that ship without bugs

**Core principle:** a plan is not done when it reads well. It is done when every
promise in it is owned by a PR row, a test, a question, or a named human with a
date. Why this pack exists, with the evidence: `why.md`.

## Vocabulary (used the same way in every skill of the pack)

- **PR row** — one line of the PR table (`templates/PR-TABLE.md`); the unit of delivery.
- **Phase** — a group of PR rows with one acceptance; the unit of acceptance.
- **Gate** — a check that can fail on its own: a test, a CI job, a screenshot a named person approves, or a PR row.
- **Plan tracker** — wherever the plan is published (wiki, tracker, plan app). If none, the plan file in git.

## The route (do not skip or reorder)

| # | Phase | Skill | Produces |
|---|---|---|---|
| 1 | Ground truth | `plan-ground-truth` | `sources/` (CONTEXT, audits, screenshots, PROBES, NOT-READ), `COVERAGE.md`, scope confirmed |
| 2 | Draft | `plan-dual-draft` | `BRIEF.md` → `plan-A.md` + `plan-B.md` → `plan-merged.md` → `review.md` → `dialog.md` → **draft verdict** |
| 3 | Gates | `plan-acceptance-gates` | acceptance per phase edited **into `plan-merged.md`**; `MATRIX.md` (linked) |
| 4 | Slicing | `plan-slicing` | the PR table as the `## Tasks` section of `plan-merged.md` |
| 5 | Readiness | `plan-readiness-review` | one knock-down pass on what phases 3–4 added, then `READINESS.md` + **final verdict**; the passing body is copied to `PLAN.md` |
| 6 | Handoff | `plan-execution-handoff` | one `EXECUTOR-BRIEF` per agent, `EXECUTION-LOG.md`, merge policy |

Phases 3–4 are edited by the planner who merged (resumed), and attacked once
more in phase 5 by the reviewer who did not write them. Templates for every file:
`templates/`.

**Small plan** (3–5 PRs, one repo): phases 1, 3, 4, 5 are mandatory; phase 6 whenever anyone other than the planner executes. Phase 2
becomes one planner covering both angles + one knock-down reviewer
(`plan-dual-draft/prompts.md`, "Single planner").

## Files

```
<plan-dir>/
  sources/  CONTEXT.md  audit-*.md  PROBES.md  NOT-READ.md  screenshots/
  COVERAGE.md  BRIEF.md  diffs.md
  plan-A.md  plan-B.md  plan-merged.md  review.md  dialog.md
  MATRIX.md              # the file; plan-merged.md links to it, never copies it
  decision-record.md     # only when the two drafts agree (plan-dual-draft step 3b)
  review-2.md  dialog-2.md  READINESS.md
  PLAN.md                # decisions + criteria + ## Tasks (the PR table)
  briefs/<agent>.md  logs/PR-<n>.done  EXECUTION-LOG.md
```

## Hard gates (checked line by line in `plan-readiness-review`)

1. Sources on disk and mapped in `COVERAGE.md` — nothing from memory.
2. Scope confirmed, or **one example** shown before any fan-out.
3. Every flag / second code path has a flip PR row, owner, date, exit.
4. Every phase is accepted on the running build (UI: production build, zero console errors, screenshot per band; pipeline: a row or log line with a correlation id on the production route).
5. Every unknown limit is a Phase-0 measurement.
6. Every shared artifact has exactly one owner PR row.
7. Every review finding is a PR row, a question, or "won't do + consequence".
8. Every decision owned by someone else is a posted question, not answered by the planner.
9. Every human gate (device, design sign-off, secret, external config, approval) has a name and a date, scheduled first.
10. Branch protection, CI duration and release gates in repo docs were probed; the merge path is written.

**One example** = one filled artifact the requester can react to: an annotated
screenshot of one screen, one section of `sources/CONTEXT.md`, or the first
three rows of the PR table. A summary of intentions does not count.

## Stop rules

- The phase-2 YES only closes the draft. Planning is done when `READINESS.md`
  says **YES + at most 3 residual risks, each with an owner**.
- One "more detail" round is allowed, only for sections an executor could not
  implement without guessing (no file path, no acceptance, no owner). A second
  round needs the requester.
- If a source could not be read, say so in the plan header. Never fill the gap with a guess.
- After the first publish, expect one revision from the decider's review
  (`plan-readiness-review` → Revisions): keep the 10 % of effort the Budget leaves
  free for it.

## Budget (so no phase eats the run)

Phase 1 ≤ 30 % of the effort, phase 2 ≤ 30 %, phases 3–5 ≤ 30 %. Plan body ≤ 60 KB by default; going over needs one line of reason in `READINESS.md`. The merged draft takes at most three quarters of the 60 KB; gates and slicing fill the rest. A revision after the decider's review can add a quarter more (one run: 59 → 74 KB) — give the reason line then.
Heavy agents in parallel: as many as the machine's RAM allows, never more than 3
by default.
