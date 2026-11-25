---
name: branch-review-summary
description: "Summarizes provided or accessible design-branch changes for reviewers, highlighting scope, rationale, risk, and review focus. Use when branch or before/after evidence is available in the current session."
---

# Branch Review Summary

## Capability Mode

`Review available evidence only`. Do not assume the Figma Agent can access branch history, compare branches, or infer the main-file baseline.

## Required Context

At least one of:

- An accessible branch comparison
- Before-and-after frames or versions
- A supplied change list, screenshots, or reviewer notes

Without comparison evidence, return the exact inputs needed rather than inventing a diff.

## Workflow

1. Identify the compared baseline and branch state.
2. Group verified changes by flow, component, content, visual system, or behavior.
3. Explain user or engineering impact without speculating about intent.
4. Flag high-risk changes, unresolved questions, and areas requiring close review.
5. Separate verified changes from author-provided rationale and inferred implications.

## Guardrails

- Do not claim exhaustive branch coverage without branch-level access.
- Do not infer why a change was made unless documented.
- Do not treat unchanged or inaccessible areas as reviewed.

## Output Contract

Return scope, verified changes, impact, review focus, unresolved questions, evidence gaps, and an explicit coverage statement.
