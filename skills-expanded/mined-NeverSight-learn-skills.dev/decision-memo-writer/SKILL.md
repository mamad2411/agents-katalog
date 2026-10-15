---
name: decision-memo-writer
description: Write and review decision memos for product, strategy, pricing, launch, growth, design, marketplace, operations, platform, and investment choices. Use when a team needs a clear recommendation, options, tradeoffs, evidence, assumptions, risks, decision owner, reversible/irreversible classification, success metrics, and follow-up plan instead of open-ended discussion.
---

# Decision Memo Writer

Use this skill to turn ambiguous product debate into a decision-ready memo.

## Workflow

1. Identify decision owner, decision deadline, scope, stakeholders, and whether the decision is reversible.
2. Read `references/decision-memo-systems.md`.
3. Separate facts, assumptions, options, constraints, unknowns, risks, and values.
4. Compare options with evidence and second-order effects.
5. Recommend one path, define success metrics, and specify review/rollback triggers.

## Guardrails

- Do not present a brainstorm as a decision memo.
- Do not hide weak evidence, unresolved assumptions, or stakeholder tradeoffs.
- Do not force consensus when the memo needs a named accountable decision.

## Output format

```text
Decision:
Owner/deadline:
Recommendation:

Context:
Options considered:
- <option> -> benefits, costs, risks, evidence

Decision rationale:
Assumptions to validate:
Risks and mitigations:
Success metrics:
Follow-up / revisit trigger:
```
