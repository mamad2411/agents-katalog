---
name: domain-modeling
description: "Resolve shared business terms, rules, and lifecycle ambiguity; use product-spec for feature-local behavior."
---

# Domain Modeling

## Entry Gate

Resolve cross-functional language and rules only when the ambiguity spans owners or
lifecycle boundaries. Require an identified fact source and scope; do not invent
product decisions or technical design.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Shared terms, invariants, or context boundaries conflict | [modeling guide](references/modeling-guide.md) | Named glossary/context/rule facts |
| A feature-local behavior or acceptance is unresolved | [usage](references/usage.md) | Route to `product-spec` |
| Need examples and nearest boundaries | [usage](references/usage.md) | Owner decision |

## Invariants

- Keep facts, assumptions, unresolved questions, and implementation choices distinct.
- Preserve the source authority and evidence level for each conclusion.
- Do not write a competing product/UI/design contract, source change, review, or Git result.

## Output Map

Return the named fact source, terms/rules/context boundaries, source basis, unresolved
ambiguities, affected owners, and next semantic handoff.

## Reference Map

- Read [modeling guide](references/modeling-guide.md) for context, lifecycle, rule, and validation procedures.
- Read [usage](references/usage.md) for mode selection and boundaries.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
