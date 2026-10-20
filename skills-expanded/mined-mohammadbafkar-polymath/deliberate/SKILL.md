---
name: deliberate
description: Run an iterative observe-frame-options-tradeoffs-risks-revise loop for a plan, design, doc, idea, or implementation; composes brainstorm, red-team, and pre-mortem.
---

# deliberate

> A structured thinking loop for ambiguous or high-stakes work. It does **not**
> re-implement divergence or critique — it *composes* the thinking primitives
> (`brainstorm`, `red-team`, `pre-mortem`) and owns only the framing, evaluation,
> synthesis, and revision around them.

## When to use

- The user asks to think through, evaluate, review, improve, or plan a non-trivial idea, implementation, design, roadmap, or document.
- Data is incomplete and assumptions need to be named.
- The right answer may require changing direction after new evidence appears.
- The user asks for an iterative reasoning loop that diverges, critiques, and consolidates.

## What this skill owns vs delegates

| Phase | Owner |
| ----- | ----- |
| Observe, Frame | this skill |
| Diverge (generate options) | `polymath-thinking:brainstorm` |
| Evaluate (weighted comparison) | this skill, or `polymath-decisions:tradeoff-matrix` for a decision-grade matrix |
| Stress-test (adversarial critique) | `polymath-thinking:red-team` |
| Stress-test (failure modes) | `polymath-thinking:pre-mortem` |
| Revise, Consolidate | this skill |

Treat the sibling skills as the single source of their procedure — do not paste
their steps here. In a portable harness where you cannot invoke them, run their
published procedure but keep the section structure below so the result matches.

## Inputs

- Subject: plan, design, document, implementation, product idea, incident, architecture, or problem.
- Available artifacts: paths, links, issue IDs, PRs, logs, metrics, user notes.
- Decision pressure: deadline, reversibility, cost of error, stakeholders.

## Procedure

1. **Observe.** Read the relevant artifacts and project context. Separate facts, claims, assumptions, unknowns, and constraints.
2. **Frame.** State the problem in one sentence. Name goals, non-goals, success measures, and what would make the answer wrong.
3. **Diverge.** Run `polymath-thinking:brainstorm` on the framed problem to produce the option set (≥ 5 materially different options, including "do nothing / defer" and one that challenges the framing). Use its output; do not re-derive the brainstorm procedure here.
4. **Evaluate.** Pick 3–6 criteria that differentiate the options and rank them against those criteria — never a vague "fit" score. For a weighted, decision-grade comparison hand off to `polymath-decisions:tradeoff-matrix`.
5. **Stress-test.** Run `polymath-thinking:red-team` against the leading option (strongest objection, what evidence would reverse the recommendation) and `polymath-thinking:pre-mortem` against the plan that would implement it (failure modes, likelihood × impact).
6. **Revise.** If the critique invalidates the leading option, change direction. If not, strengthen the recommendation and name the residual risk explicitly.
7. **External input — only if real.** If an external model is reachable as a configured tool (e.g. an MCP server exposing another model) or the user pastes another model's output, incorporate it and attribute it by name. Absent that, you have one model: state plainly that this is a single-model analysis. Never simulate, label, or imply a second model's voice that was not actually consulted.
8. **Consolidate.** Produce a decision-ready result: recommendation and why; alternatives rejected and why; assumptions to validate; next experiment or implementation plan; validation and rollback / exit criteria.

## Output

For durable work, write `docs/thinking/<slug>-deliberation.md` with:

```markdown
# Deliberation: <subject>

## Observations
## Frame
## Options          (from brainstorm)
## Trade-offs       (from tradeoff-matrix when used)
## Critique         (from red-team + pre-mortem)
## Revision
## Recommendation
## Validation Plan
## Open Questions
```

For quick work, respond inline with the same sections compressed.

## Quality bar

- Facts, assumptions, and unknowns are visibly separated.
- At least one option changes the framing, not just the implementation.
- The recommendation can change after critique.
- Divergence and critique are sourced from the sibling skills, not re-invented here.
- No external model is claimed unless one was actually consulted.
- The result includes validation criteria and a next action, not just analysis.
