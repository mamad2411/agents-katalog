---
name: opus-magnum
description: Apply the Opus Magnum method to a task — adaptively. On invocation it triages the task, identifies which ELEMENTS apply (alignment, spec, decomposition, continuity, TDD, cross-model review, isolation, parallelism, guardrails, observability), and runs only those in the right mode — human-in-the-loop or unattended. Full autonomous backlogs run the Ouroboros loop; tasks that are not AFK-able still get the elements that fit. Use for any non-trivial build, design, or review task. Trigger — `/opus-magnum`.
---

# /opus-magnum — apply the Great Work, adaptively

> Opus Magnum is not one mode — it is a set of elements. When called, do not assume the full autonomous loop. First triage the task, then apply only the elements that fit, each in the right mode.

The core idea: keep work in the smart zone, carry context in a durable journal (the Quintessence), gate quality with feedback loops and a cross-model review (the Assay). How much of the machine you bring depends on the task.

## Step 1 — triage the task

Read the task on these axes and state your read in one line each:

- **AFK-ability** — can it run unattended to a verifiable "done"? (Strong feedback loops + clear acceptance = yes. Judgment, taste, or ambiguity = no.)
- **Code-bearing** — does it produce a reviewable diff?
- **Alignment** — is intent ambiguous or decision-heavy enough to need a structured grill?
- **Horizon** — is it long/multi-step enough that context will be lost without a journal?
- **Parallelism** — are there independent sub-tasks?

Most real tasks are mixed. A task can be "not AFK-able" overall yet still want alignment, review, and continuity.

## Step 2 — select the elements

The elements, with when each applies and its mode:

| Element | Applies when | Mode |
|---|---|---|
| **Grill** (align to a shared design concept) | intent ambiguous / judgment-heavy | HITL |
| **PRD** (destination document) | multi-step, worth a spec | semi |
| **Vertical-slice decomposition** | a buildable backlog exists | semi |
| **Quintessence** (durable journal) | long / multi-session / context will be lost | always-on |
| **Clear-and-reprime** (smart-zone discipline) | long-horizon work | discipline |
| **Alembic** (worktree isolation) | autonomous code changes | AFK |
| **TDD** (feedback-loop gating) | code-bearing | HITL or AFK |
| **The Assay** (cross-model review) | any diff, decision, or artifact worth a second model | either |
| **coniunctio** (integration/merge) | parallel branches to reconcile | AFK |
| **Guardrails** (spend / failure / safety) | anything running unattended | AFK |
| **The Coven** (up to 3 parallel Alembics) | independent sub-tasks | AFK |
| **The Speculum** (observe / feed) | a run worth watching | any |

State which elements you are bringing and which you are deliberately leaving out, and why.

## Step 3 — choose an application mode

- **Full Opus** — an AFK-able backlog of independent, verifiable tickets. Run the autonomous Ouroboros loop. This is the only mode that needs the whole machine.
- **Partial application** — the default for mixed tasks. Run just the fitting elements. Common shapes:
  - **Align-and-spec**: Grill → PRD → decomposition, then stop (hand the backlog back, or feed it to a later Full Opus run).
  - **Pair-build** (not AFK-able, but code): human and Claude build it together with TDD + the Assay on each diff + Quintessence journaling — no unattended loop.
  - **Review-only**: run the Assay over an existing diff or artifact; report findings; fix interactively.
  - **Continuity-only**: keep a long, hands-on session in the smart zone — journal decisions to the Quintessence and clear-and-reprime between phases, without any autonomous coding.
- **Escalate / de-escalate mid-task** — if a "pair-build" turns out to be cleanly AFK-able, promote it to a Full Opus ticket; if a Full Opus ticket hits a judgment call, drop to HITL for that decision, then resume.

## Step 4 — run the applicable elements

Run HITL elements interactively (the human drives the grill, the design decisions, the QA). Run AFK elements through an engine or a disciplined print-loop. Journal throughout, so even a hands-on session leaves a Quintessence trail. Honor the guardrails on every unattended spawn.

## Running without the engine

The method does not require the reference engine. The manual equivalents:

- **Quintessence**: a `QUINTESSENCE.md` at repo root. Append decisions, state, and next-steps after each work phase. Prime every fresh session from it.
- **Clear-and-reprime**: when a phase completes, journal, then `/clear` and re-prime from the journal + the next ticket. Never ride one degrading context.
- **Backlog**: `issues/NNN-title.md` files, each tagged `## Type` `AFK` or `HITL`, with acceptance criteria and blockers.
- **Alembic**: `git worktree add` per ticket; work in isolation; merge to an integration branch; human approves promotion to `main`.
- **The Assay**: run a second model (e.g. Codex CLI) over the diff before accepting it. Hard gate when available, advisory when not.
- **Guardrails**: spend cap, halt after N consecutive failures, never force-push / deploy / touch secrets unattended, and never accept a "passing" ticket whose branch diff is empty.

## Alchemical vocabulary

Opus Magnum (the system) · Quintessence (the journal) · Ouroboros (the loop) · Alembic (a worktree vessel) · the Assay (the review gate) · coniunctio (the merge) · the Speculum (the dashboard). Ticket lifecycle: calcinatio → solutio → separatio → coniunctio → coagulatio.
