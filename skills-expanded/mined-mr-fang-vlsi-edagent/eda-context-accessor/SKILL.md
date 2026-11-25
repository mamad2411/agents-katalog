---
name: eda-context-accessor
description: Retrieve scoped knowledge-base context and tool-registry reuse evidence for an EDA task, then emit compact context artifacts that downstream skills can consume directly.
---

# EDA Context Accessor

## When to use

Use this skill when a task needs shared KB retrieval, tool-catalog reuse checks, or both, and you do not want each downstream skill to restate that logic.

## Scope Boundary

This skill owns:
- scoped KB context loading,
- scoped tool-registry reuse queries,
- compact context artifact generation for downstream skills.

It does not own:
- final domain conclusions,
- execution gating,
- code implementation,
- routing policy.

## Expected Downstream Consumers

Typical consumers include:
- `workflow-router` before routing when shared KB/tool context is needed,
- execution skills that need scoped KB evidence without duplicating retrieval logic,
- theory-analysis skills that need professional background evidence before judgment,
- `eda-infra-maintainer` when retrieval reveals KB/tool maintenance work.

## Inputs

Provide or derive:
1. task scope and objective,
2. keywords or topic names for KB retrieval,
3. keywords for tool reuse query,
4. expected downstream consumer skill(s).

## Outputs

Return or update:
- `kb_context.md` or equivalent scoped context note,
- tool-query evidence (`tool_query.tsv` or cited terminal result),
- concise reuse recommendation for downstream skills,
- `kb_feedback_decision` with one of: `none`, `maintain`, `update`, `overturn`, `add`,
- `kb_feedback_reason` tied to affected KB files or missing areas.

## Hard Rules

1. Prefer local KB and tool-registry evidence before inventing new scripts or assumptions.
2. Keep retrieved context scoped to the current task; do not dump unrelated KB content.
3. Distinguish retrieved facts from downstream inferences.
4. Every handoff must include an explicit KB feedback recommendation, even if the decision is `none`.

## Operational References

1. Load `references/kb-context-loading.md` when the task needs scoped KB retrieval or evidence-gap context.
2. Load `references/tool-reuse-query.md` when the task may reuse an existing tool or when a downstream skill is considering a new script/helper.
3. Load `references/output-contract.md` when a downstream skill needs a reusable context artifact rather than raw terminal output.
4. Load `references/kb-feedback-policy.md` when deciding whether the current KB should be maintained, updated, overturned, or expanded.
