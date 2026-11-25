# Cross Tab Compare

## When To Use

Use this skill when the task requires collecting evidence from multiple tabs or pages before comparing or synthesizing a result.

Use it for workflows where evidence must be gathered from more than one location before a conclusion is valid.

Do not use it for:

- single-page summarization
- continuation editing
- tasks where comparison is incidental and not the core workflow

## Procedure

1. Identify every comparison target up front.
2. Visit each target and collect the requested facts before drawing conclusions.
3. Normalize observations into notes using stable labels.
4. Compare only after all required facts are gathered.
5. If one target cannot be read, report partial completion rather than inventing a comparison.

## Required Evidence

- A fact set for each comparison target
- Normalized notes or labels for each fact
- Final comparison based on gathered evidence

## Common Failures

- Comparing after reading only one target
- Mixing values from different tabs without labels
- Losing a fact when switching tabs or pages

## Verification

- Prefer deterministic checks that each requested target was visited and each requested fact was captured before producing the comparison.

## Relevance

This is a strong reusable skill because cross-page and cross-tab comparison is a stable browser-agent workflow.

Current strongest E2E targets:

- `tests/e2e/continuation-cross-tab.test.ts`
- `tests/e2e/continuation-paginated-memory.test.ts`

Additional candidate targets:

- `tests/e2e/article-research.test.ts`
- `tests/e2e/job-board.test.ts`
