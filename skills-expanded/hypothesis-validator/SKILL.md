---
name: hypothesis-validator
description: "Use for decision-grade startup hypothesis validation: kill/refine ideas, identify ICP, jobs, demand, money signals, wedges, and GTM paths via the bundled Russian research prompt."
---

# Hypothesis Validator

## Canonical Prompt

Before performing the task, read
`references/hypothesis-validator-v2.md` in full.

Treat that file as the complete and authoritative operating prompt.

Do not summarize, rewrite, translate, shorten, reorder, normalize Markdown, or
improve the canonical prompt. Execute it as written.

## Inputs

Use the user's provided values for:

- `{ГИПОТЕЗА}`
- `{КОНТЕКСТ_И_ОГРАНИЧЕНИЯ}`

If the hypothesis is missing, ask for it. If additional context and constraints
are missing, proceed only when the user has clearly provided enough context or
explicitly asks to run without extra context.

## Output

Follow the output contract, structure, tone, and decision criteria defined in
`references/hypothesis-validator-v2.md`.
