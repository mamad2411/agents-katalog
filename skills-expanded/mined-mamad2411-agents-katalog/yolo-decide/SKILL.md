---
name: yolo-decide
description: Use when facing a design or architecture decision that benefits from multiple perspectives before committing. Produces a decision record under workspace/decisions/. Triggers on "help me decide X vs Y", "which approach", "should we use A or B".
---

# yolo-decide

Reach a defensible decision via multi-perspective analysis, and record it.

## Procedure
0. The multi-perspective analysis runs at the billed `agents.decide` tier. Confirm the decision framing before launching it — the plan-gate analogue for a decision (`.claude/yolo/conventions.md` *The two gates*). **STOP and wait for the human here** (state the framing, then pause) — do not state the framing and slide into the analysis in the same turn. Skip only if the user pre-consented.
1. State the decision and the options crisply.
2. Argue each option from several lenses — at minimum correctness/risk, simplicity/maintainability, and pragmatism/cost. Surface the strongest case FOR and AGAINST each.
3. Recommend one option, with explicit rationale, the alternatives considered, dissents (minority concerns worth recording), and revisit triggers (conditions that should reopen this).
4. Write `workspace/decisions/<slug>.md` with: decision, rationale, approach, alternatives_considered, dissents, revisit_triggers, confidence. Confirm before overwriting an existing slug.
5. Commit (`yolo: decision <slug>`).

## When to reach for `bakeoff` instead
`yolo-decide` is a single-pass, multi-lens analysis — right for most X-vs-Y calls. For a **high-stakes,
hard-to-reverse decision with several defensible options** (architecture, migration, tool selection), the
[`bakeoff`](https://github.com/CoriChui/bakeoff) skill runs a heavier judged tournament: it generates
diverse candidate solutions, auto-derives a rubric for the problem, scores each with independent judges,
and adversarially refutes the leader. If `bakeoff` is installed, offer it for those cases, then record its
verdict as the decision here (`workspace/decisions/<slug>.md`) so the trail stays in one place.

## Constraints
- Read-only with respect to code; the only file you write is the decision record.
- No status field; decisions are standalone records.
- Run the multi-perspective analysis at the `agents.decide` tier from `workspace/config.yaml`.
