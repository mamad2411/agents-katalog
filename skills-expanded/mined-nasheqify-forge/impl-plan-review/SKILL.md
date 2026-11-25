---
name: impl-plan-review
description: >
  Multi-perspective review of an implementation plan BEFORE coding — validate the
  implementer's reading of the spec before code is written. Triggers when an MCA
  implementation plan must be validated before coding (build execute,
  conditional); NOT for spec review (use spec_board) or code review (use
  code_review_board).
status: active
relevant_for: ["main-code-agent"]
invocation:
  primary: workflow-step
  secondary: [user-facing]
disable-model-invocation: false
uses: [_protocols/discourse, _protocols/context-isolation, _protocols/dispatch-template]
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: impl-plan-review

## Purpose

MCA writes an implementation plan (module structure, key
decisions, data flow). 2-3 code agents review this plan before
coding starts. It catches misinterpretations of the spec,
suboptimal architecture decisions, and forgotten constraints —
BEFORE code exists.

"Plan approval is the cheapest gate." (Osmani)

## When to call

- Standard path: after DELEGATION (step 11), before IMPLEMENT
  (step 12).
- Full path: after DELEGATION (step 17), before IMPLEMENT (step
  18).
- Direct path: NOT (no plan on trivial scope).

**Trigger check (Buddy):** does the task have a spec with ≥3 ACs
OR a schema change OR cross-module impact? → impl_plan_review.
Otherwise skip with rationale.

**Bedrock (why this trigger):** facets per
`agents/buddy/multi-perspective.md` —
primarily **blind-spot compensation** (MCA's interpretation of spec
degrees-of-freedom needs reviewer-diversity before code locks it)
and **complexity mastery** (multi-decision plans exceed solo
synthesis reliability). The count is the fallback when facets are
unclear, not the gate. Facet-question first, count as net.

## Input

MCA writes an implementation plan first in full_plan step 1
(plan). That plan undergoes review BEFORE step 3 (implement).

**MCA implementation-plan format (MUST):**
- **Module structure:** files created / changed, package
  assignment.
- **Key decisions:** implementation decisions + rationale
  (patterns, algorithms, error handling).
- **Data flow:** input → processing → output across modules.
- **Spec interpretation:** the spec's degrees of freedom and how
  MCA interprets them.
- **Risks:** what could go wrong? Where is the implementation
  fragile?

## Agents (board pattern, code-review pool)

- **code-review** (ALWAYS, architecture axis): module structure,
  dependency graph, pattern fit. (Code-review absorbed
  code-architecture.)
- **code-adversary** (ALWAYS): edge cases, smart-but-wrong
  interpretations.
- **code-domain-logic** (conditional, on business logic):
  state-machine correctness.

Min 2 agents, max 3. Dispatch via
`_protocols/dispatch-template.md` (anti-bias).

## Flow

```
1. MCA writes the implementation plan (full_plan step 1).
2. Assemble agent prompts:
   - read agents/_protocols/reviewer-base.md
   - read agents/_protocols/code-reviewer-protocol.md
   - read the agent persona (e.g. agents/code-review.md for the architecture axis)
   - dispatch via _protocols/dispatch-template.md (anti-bias)
3. Dispatch 2-3 agents in parallel (context-isolated).
   Input: implementation plan + spec + delegation artifact.
4. Buddy reads the reviews directly (no chief — analogous to code_review_board L1).
5. [Optional] discourse on contradictory reviews.
6. Gate decision.
```

## Gate

```
APPROVED:  0 critical, 0 high → MCA starts coding (full_plan step 3)
REVISE:    ≥1 high → MCA revises the plan, another review (max 2 iterations)
REJECT:    ≥1 critical OR after 2 REVISE iterations → Buddy escalates to user
```

## Output paths

```
docs/reviews/impl-plan/
  {task-id}-{role}.md         agent reviews
  {task-id}-discourse-*.md    discourse (when run)
```

## Integration into full_plan

`full_plan` step 1 (plan) stays. NEW: step 1.5 plan review (this
skill) between step 1 and step 2 baseline. Only after APPROVED
does the workflow proceed. Sequence: step 1 plan → step 1.5
review → step 1b fact-check → step 2 baseline (`@code-spec-fit`
conditional when `spec_ref` is set) → step 3 implement (MCA codes).

## Contract

### INPUT
- **Required:** MCA implementation plan (module structure, key
  decisions, data flow, spec interpretation, risks).
- **Required:** spec (`spec_ref` from the task YAML) — for
  spec-interpretation validation.
- **Required:** delegation artifact — for done-criteria
  reconciliation.
- **Optional:** frame report (from `frame`) — as context.
- **Context:** `agents/_protocols/reviewer-base.md`,
  `code-reviewer-protocol.md`, `dispatch-template.md`.

### OUTPUT
**DELIVERS:**
- Gate decision: APPROVED (0C+0H) / REVISE (≥1H) / REJECT (≥1C
  or after 2 REVISE).
- Agent reviews: 2-3 code-agent reviews under
  `docs/reviews/impl-plan/`.
- Findings with severity, affected plan aspects, concrete
  revision hints.

**DOES NOT DELIVER:**
- No code review — checks the PLAN, not the code.
- No spec review — takes the spec as given; checks the
  interpretation.
- No chief consolidation — Buddy reads directly (analogous to
  code_review_board L1).

**ENABLES:**
- Build implement: APPROVED → MCA starts coding.
- Plan revision: REVISE findings as structured input for MCA.
- Spec feedback: misinterpretations as a signal for spec
  sharpening.

### DONE
- Gate decision taken: APPROVED or REJECT.
- Agent reviews persisted under `docs/reviews/impl-plan/`.
- On discourse: discourse files persisted.

### FAIL
- **Retry:** REVISE → MCA revises the plan → re-review (max 2
  iterations).
- **Escalate:** REJECT (≥1C) or after 2 REVISE iterations →
  Buddy escalates to the user.
- **Abort:** not foreseen — escalate to the user instead of
  aborting.

## Boundary

- **No code review** — this checks the PLAN before coding;
  `code_review_board` checks the CODE after coding.
- **No spec review** — spec verification is `spec_board`'s job;
  this skill takes the spec as given and checks the
  interpretation.
- **No own chief** — scope is small enough for Buddy to read
  directly; no chief consolidation.
- **No convergence loop** — max 2 REVISE iterations, then escalate
  to the user.

## Anti-patterns

- **NOT** trigger `impl_plan_review` on trivial scope. **INSTEAD**
  trigger check (≥3 ACs OR schema change OR cross-module impact).
  Because: overhead without gain on simple tasks.
- **NOT** review the plan without giving the spec as input.
  **INSTEAD** spec + plan + delegation artifact in parallel to
  the reviewer. Because: spec interpretation cannot be validated
  without the spec.
- **NOT** keep looping after 3+ REVISE iterations. **INSTEAD**
  escalate to the user after 2 iterations. Because: persistent
  disagreement signals an unclear spec or wrong agent fit.
- **NOT** ignore REVISE feedback and code anyway "because the
  reviewers misunderstood". **INSTEAD** revise the plan or
  document explicitly why the feedback doesn't apply. Because:
  plan review is the cheapest gate — skipping disagreement costs
  multiple times more later in the code review.
