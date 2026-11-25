---
name: plan-dual-draft
description: "Use to draft a large plan with two independent planner agents — shared brief, blind drafts from different angles and models, an optional cross-read, a merge that picks instead of averaging, an adversarial review that tries to knock the plan down, a written dialog where the author may argue back, and a consistency pass with a draft verdict. Use after plan-ground-truth. Skip for editing an existing plan; for a small plan use the single-planner prompt in prompts.md."
author: SamuelStefano
tags: [planning, multi-agent, review, architecture]
---

# Two planners, one plan

**Core principle:** disagreement is the product. Two blind drafts surface the
decisions; the merge records them; the review attacks them; the dialog lets the
right side win with a source.

Measured run: 22 minutes, 20 ADRs, 26 findings (22 accepted, 4 partial), 5 new
inconsistencies caught by the final pass, verdict YES.

## Roles

| Role | Model | Job |
|---|---|---|
| Orchestrator | any | writes `BRIEF.md`, launches, waits on files, never reads 120 KB |
| Planner A | strongest reasoning model | angle 1 (architecture, data, collaboration) — covers every section |
| Planner B | a **different** model | angle 2 (experience, visuals, performance) — covers every section |
| Merger | A, resumed | one plan, decisions as ADRs |
| Reviewer | B, resumed | knocks the merged plan down |

Resume the same agents (they keep their plan in context). Known bias: B reviews
a plan that contains half its own ideas — the hunt list below counters it by
asking explicitly for depth lost from **both** drafts.

## Step 1 — `BRIEF.md`

Fill `brief-template.md`. Both planners read it by path.

## Step 2 — Blind drafts

"Do **not** read the other plan." Each ends its file with `<!-- PLAN-DONE -->`
and replies with 5 lines: its 5 most confident decisions. The orchestrator saves
both replies to `diffs.md` — the disagreement list, on record before any exchange.

## Step 3 — Choose the flow

| Flow | When | Steps |
|---|---|---|
| **Default** (measured) | always, unless below | 3b if the drafts agree → merge → knock-down → dialog → close-out |
| **Cross-read** (the requester's original method; **unmeasured** — record whether its disagreements survived to ADRs) | the requester asks for it, or the two angles barely overlap | each planner reads the other plan and appends what it lacks under "Adopted from X", changing nothing it already decided → A merges; every line of `diffs.md` becomes an ADR → knock-down → dialog → joint close-out |

Never let two agents edit the same file. "Together" means turns in `dialog.md`.

## Step 3b — When the drafts agree, attack the agreement

Two drafts choosing the same architecture is not confirmation; it is one shared
premise. Before the merge, give the choice to a red-team whose only job is to make
the best case for the alternative, plus one lens per risk the angles did not cover
(schema and security; the person who authors or operates it) — at most 3 agents.
The orchestrator checks every disputed fact in the code and writes
`decision-record.md` (locked facts, final decisions, dissent), ending
`<!-- DR-DONE -->`; the merge treats it as binding.
Trigger: `diffs.md` shows the same top-level choice in both replies.
*(Both planners picked the same architecture. A red-team and two lens agents then
showed a draft could leak through an anonymous endpoint, a seeder would rewrite the
published copy, and both drafts' enrolment rules were wrong in opposite directions.)*

## Step 4 — Merge (picks, never averages)

- Where the drafts differ, pick one and record an ADR; the loser goes under *Alternatives*.
- Say which planner owns which depth ("keep B's screens, keep A's data rigor").
- Top section: "What came from where (A/B)".
- Size budget (default 60 KB): cut prose, **never drop a whole section**.
  *(The merge dropped "first tasks"; no tasks were ever created.)*
- The merge takes at most **three quarters** of the budget. Gates and slicing add
  the rest. *(A 52 KB merge became 68 KB after phases 3–4 and was trimmed while a
  reviewer was already reading it.)*

## Step 5 — Knock-down review

B does **not** edit. `review.md`: `B#N — BLOCKING|IMPORTANT|MINOR — section/ADR — what is wrong — concrete fix`.
Hunt list: in `prompts.md`. It includes every gate of `plan-acceptance-gates`
that is still prose.

## Step 6 — Dialog

A answers each item in `dialog.md`: `B#N — ACCEPTED|PARTIAL|REJECTED — reason`, then edits.
- A may argue back; "X exists / does not exist" needs a source on either side.
  *(Two review claims were wrong; the defended feature shipped as planned.)*
- Reviewers never flip a **preference** question (language, tone, taste)
  without evidence of what the requester wants — keep both reasons in the question.

## Step 7 — Close-out

B replies to rebuttals, applies the smallest open fix, runs a **consistency
pass over the whole plan** (edits create new contradictions), runs
`format-check.md`, and ends with `Draft verdict: YES|NO` + at most 3 risks.
Joint close-out (cross-read flow): one extra turn each in `dialog.md`, at most
one "more detail" round (see `complex-plan` stop rules).

The draft verdict closes phase 2 only. Phases 3–4 follow; the final verdict is
in `plan-readiness-review`.

## Coordination

- Files, not status: markers `PLAN-DONE`, `CROSS-DONE`, `MERGE-DONE`, `REVIEW-DONE`, `DIALOG-DONE`; wait with `until grep -q <marker> <file>; do sleep 15; done`.
- The marker is the agent's **last** write: no edit after it. An agent that trims
  or condenses afterwards removes the marker first and writes it again at the end.
  *(A reviewer read the file at 68 KB while its author was cutting it to 61 KB;
  every finding had to be re-checked against the file on disk.)*
- After resuming an agent, confirm its output file appears; a message that arrives
  while it is still closing a turn may never be picked up — send it again.
- Tell every reviewer which commit the plan's citations were read at.
- Replies capped at 3–5 lines.
- Publishing: see `plan-readiness-review`.
