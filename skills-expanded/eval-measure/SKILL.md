---
name: eval-measure
description: Use when the user asks if an AI app is measured correctly, needs Galileo metrics, expected-output contracts, metric profiles, eval gates, or measurement before optimizing.
---

# Eval Measure

Use this skill before optimization or broad fixture work. Its job is to make the
measurement contract explicit.

## Required Reference

Use `skills/eval-engineer/references/metric-profile-checklist.md` and
`skills/eval-engineer/assets/metric-profile-template.md`.

## Do

- Define risk profile and quality dimensions.
- Write the full expected-output contract: expected decision, required and
  forbidden citations, tools, answer constraints, abstention, permissions, and
  safety requirements.
- Include retrieved-source gates when source authority matters:
  `required_retrieved_sources`, `forbidden_retrieved_sources`, and whether
  final citations alone are sufficient for the case risk.
- Prefer independent observations over agent self-reports for safety gates.
  Check answer text, citations, retrieved source IDs, tool calls, and Galileo
  scorers before accepting flags emitted by the app under test.
- Choose Galileo metrics by failure contract, not by one global list.
- Identify metric gaps before accepting a cost or quality change.

## Gotchas

- Agent self-reported flags are instrumentation breadcrumbs, not acceptance
  evidence.
- Final citations alone are not enough when retrieved-source authority is part
  of the risk.
- Do not infer latency, wall time, tokens, or cost as quality metrics.

## Validation Loop

Before finalizing a metric profile, check it against
`skills/eval-engineer/references/metric-profile-checklist.md` and confirm the
profile names quality gates, cost/performance metrics, segment gates, metric
direction, and known gaps.

## Output

Findings first. Start with the highest-risk metric gaps and the keep/reject/
inconclusive measurement decision, then produce a metric profile or explain
what evidence is missing. Do not improve the app until the expected-output
contract and acceptance gates are clear.
