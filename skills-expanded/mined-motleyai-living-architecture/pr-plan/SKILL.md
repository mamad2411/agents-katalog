---
name: pr-plan
description: Stage 1 of 4 of the /la:pr flow — interview the user to turn the tracker issue + typed brief into a detailed spec, Codex-review the plan, emit the OpenSpec change (OpenSpec repos only), and make the plan durable. Normally dispatched by /la:pr; if the /la:pr context (BRANCH, CHANGE_ID, OPENSPEC, tracker issue) is not already loaded in this session, invoke the la:pr skill instead.
---

**Stage 1 of 4 of the `/la:pr` flow.** Prerequisite: `/la:pr` has run in this
session, preflight included, and established `BRANCH`, `CHANGE_ID`, `OPENSPEC`, and the full tracker
issue (body + comments), if there is one. If any of that is missing, invoke the `la:pr` skill
instead — it rehydrates and dispatches back here. The `/la:pr` stopping policy
applies throughout this stage.

## Step 1 — Combine and interview

Treat the tracker issue body + comments AND whatever I typed when invoking
`/la:pr` as the combined brief. In case of conflict, what I typed has higher
priority but ask to be sure.

**Living-architecture repos**: the `la:living-architecture` skill's "Working
under the architecture" rules apply before drafting. The plan MUST state which element
principles apply, and any arc42 contradiction is raised as its own interview
point. If the change adds a capability, the plan also records where its spec attaches: one element's metadata `specs`
(at any depth), or `cross_cutting_specs` in `index.yaml` with a `touches:` list. When an arc42 axiom edit is needed, keep the clause **concise
and simple** — introduce a named concept (with a one-symbol gloss where it
helps, e.g. `a.b.a ≡ a`) and reference it, rather than spelling the mechanism
out inline. Present the exact wording for approval before it lands, and prefer
the shortest phrasing that stays precise.

Interview me in detail.
Cover implementation approach, edge cases, gotchas, design choices, tradeoffs, and constraints.
Skip obvious questions.
Ask one at a time and build on my answers.

**IMPORTANT — WHENEVER you ask me to make a choice, you MUST give, for the
decision, explicit PROS and CONS of each option AND a clear RECOMMENDATION of
which one you'd pick and why. This is non-negotiable. Never present options as
a bare menu. If you use a structured/multiple-choice prompt, spell out the
pros, the cons, and the recommendation inside it — do not rely on a one-line
description to carry them.**

**Genuine options only.** Ask only about genuine choices, and offer only
options a reasonable person could pick:
- **Effort is not a trade-off.** Less work or a smaller diff is never a pro,
  and more work (churn, re-blessed goldens, many call sites, plan edits) is
  never a con, unless the amount is ridiculously large. An option whose only
  advantage is less work is a strawman: never offer it.
- **No regressions.** Never offer an option that breaks or loses something
  that works today (a behaviour, a check, an output a golden pins) unless
  there is a very good reason, stated as its pro.

When only one option survives, it is not a question: take it, log it as
`(default)` and move on. This governs how you form the RECOMMENDATION above,
and applies at every stage of the flow, not just planning.

**Design bias — structural fix over band-aid.** When the brief is a bug, a
gap, or an inconsistency, decide BEFORE designing the fix whether the reported
symptom is one instance of a deeper structural cause — judged against the
principles/axioms in the `architecture/*.arc42.md` files (an axiom-violating
shape left standing, two code paths that must agree by hand, a missed
normalization that a single canonical representation would obviate, a check
repeated at every call site, etc. are all tells). Prefer a design that makes
the whole bug CLASS impossible or hard to recur — at the planner / type /
canonical-representation level, one code path instead of N — over patching
the instance in the existing repetitive implementation. This is NOT an
interview question: decide it and state the symptom, the structural cause and
the arc42 grounding in the plan. Never offer an option whose only pro is a
smaller diff. Ask only when the structural fix's diff is HUGE — then: do it
now / leave it / separate issue. Only if the problem is genuinely local with no
structural cause is the local fix the right plan.

When you think you have enough information, return a detailed, complete spec.
In the spec you write, NEVER take shortcuts or make simplifications or
extensions to the original requirements without asking me about each one first.

The spec ends with a **decisions log**: one entry per choice made while
planning, giving the decision, the options weighed, the one taken and why, and
who took it: `(user)` for a choice I made, `(default)` for one you took because
it had an obvious default, `(codex)` for a Codex finding folded in. Every
shortcut, simplification or extension I approved is an entry too. Every exact
wording I approved (an arc42 clause, a skill or finding text) is quoted
verbatim and tagged `(user, approved wording)`.

## Step 2 — Codex review of the plan

**Codex follows `reviewers.codex`.** If `la-config get reviewers.codex` prints `false`, skip this step. Otherwise, if the Codex MCP server (`mcp__codex__codex`) is not available, STOP and tell me: this repo requires Codex reviews, so never skip one silently.

Once I've approved the spec/plan, hand the plan text to the codex MCP server
(`mcp__codex__codex`) and ask it to review the plan itself — not a diff —
focusing on correctness of approach, missed edge cases, risky design choices,
test coverage gaps, and anything that contradicts the tracker issue. Codex
should not modify files; it should return actionable findings.

Bring Codex's findings back to me and discuss them. For each finding, decide
together whether to fold it into the plan, defer it, or reject it. Update the
written spec to reflect the resolved decisions before moving on, and log every
finding in the decisions log: folded ones as `(codex)` entries, rejected ones
as `rejected (codex)` with the reason, and deferred ones with the existing
tracker issue that covers them (search first; a new issue needs my yes).

## Step 3 — Emit the OpenSpec change (OpenSpec repos only)

Skip this whole step unless `OPENSPEC=1` (set by `/la:pr`). Turn the approved,
Codex-resolved plan into an OpenSpec change — but do NOT hand-author the files
from memory. OpenSpec ships authoritative, version-correct, per-artifact
instructions; follow them so the output passes `validate --strict`.

1. **Scaffold:** `openspec new change <CHANGE_ID>` (creates
   `openspec/changes/<CHANGE_ID>/.openspec.yaml`; artifacts are added next).
2. **Author each artifact in dependency order** — proposal → specs → design →
   tasks. For each, run `openspec instructions <artifact> --change <CHANGE_ID>`
   and obey the emitted `<instruction>` + `<template>`, writing to the `<output>`
   path it names. `openspec status --change <CHANGE_ID>` shows what's done/blocked.
   Most of this is a reformat of the plan — don't re-derive it:
   - **proposal.md** — `## Why` + `## What Changes` (from the tracker issue +
     plan), plus `## Capabilities` (New/Modified — this list decides which delta
     files must exist) and `## Impact`.
   - **specs/<capability-path>/spec.md** (the delta — the crux) — one file per
     capability from the proposal, using `## ADDED` / `## MODIFIED` / `## REMOVED`
     / `## RENAMED Requirements`. A **new** capability's file also needs a
     `## Purpose` (50+ chars) — omit it for an existing capability, else `archive`
     stamps a `TBD` placeholder into the corpus. Each requirement is
     `### Requirement: <name>` in
     SHALL/MUST language with **≥1** `#### Scenario:` in WHEN/THEN form. Validator
     gotchas: scenarios need **exactly four** `#` (three or bullets fail
     silently); MODIFIED must contain the FULL updated requirement; REMOVED needs
     **Reason** + **Migration**; RENAMED uses FROM:/TO:. These scenarios ARE the
     acceptance criteria for the `pr-tests` stage.
   - **design.md** — its `## Decisions` is the decisions log, keeping each
     entry's tag; approved scope cuts also go under Non-Goals. Skip design.md
     only if the log is empty.
   - **tasks.md** — the `- [ ]` checklist that also drives the
     `pr-tests` and `pr-implement` stages; maintain it here, not twice.
3. **No spec-level behaviour change?** (pure refactor, tooling, docs, or a fix
   that doesn't alter specified behaviour) — do NOT invent a requirement; set
   `skip_specs: true` in `openspec/changes/<CHANGE_ID>/.openspec.yaml`. Specs
   describe behaviour, so if behaviour doesn't change, no spec should.
4. **Gate before writing any tests:**

   ```
   openspec validate <CHANGE_ID> --strict
   ```

   Fix until green. This catches a malformed plan and — crucially — any MODIFIED
   requirement that no longer lines up with the current corpus (spec drift), at
   plan time, for free.

## Step 4 — Make the plan durable, then hard stop

> **🛑 HARD STOP (reset point 1 of 3) — before tests.** First make the plan
> durable: if `OPENSPEC=1` it's the validated change folder; if `OPENSPEC=0`,
> post the finalized plan, decisions log included, as a comment on the tracker issue (Linear:
> `mcp__linear__save_comment`; GitHub: `gh issue comment <N>`) so a reset
> recovers it. Then say we're at reset point 1 and STOP — do not start writing tests.
> I'll `/clear` and re-invoke `/la:pr`, which will detect and run
> `pr-tests`.
