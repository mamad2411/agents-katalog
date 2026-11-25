---
name: workflow-research-chain
description: "Run a full EDA research chain from knowledge exploration and paper triage to idea debate, hypothesis experiment design, implementation, git versioning, validation, and retrospective. Use when the user requests an end-to-end EDA research workflow rather than a single isolated execution step."
---

# Workflow Research Chain

## When to use

Use this skill when the user asks for an end-to-end research workflow, not a single isolated experiment step.

## Scope

This skill is the workflow owner for the full research chain and delegates each stage to specialized skills.
Global governance still follows `AGENTS.md`.

`workflow-scoped-execution` is not the owner of this workflow. It is only a delegated subworkflow when one chain stage needs governed execution.

## Inputs

Provide or derive:
1. chain objective and target question,
2. chain tag or workspace name,
3. required validation/promotion standard,
4. whether milestone reporting artifacts are expected.

## Knowledge And Tool Interaction

1. If the chain needs shared KB context loading or shared tool-reuse evidence, delegate that retrieval step to `eda-context-accessor`.
2. If `eda-context-accessor` returns `kb_feedback_decision != none`, carry that feedback into chain artifacts and schedule KB/infrastructure follow-up instead of dropping it.
3. Use `control-knowledge-explorer` when evidence is fragmented or stale and needs deeper gap mapping rather than simple context loading.
4. Write chain outcomes back into durable project memory:
- chain workspace artifacts,
- `docs/knowledge_base/90_HYPOTHESIS_VALIDATION_LOG.md` for tested hypotheses,
- maintenance log updates when the chain changed infrastructure behavior.
5. When an execution stage finishes, route reusable empirical evidence through `eda-experiment-phenomenology-analyst` so later chain stages and future chains can reuse `result/conclusion/experience` artifacts without reparsing raw logs.

## Example invocation

`Run a full research chain to explore gate-sizing strategies for power reduction on the skywater130 PDK.`

This should trigger the full workflow: chain setup, knowledge-gap mapping, literature retrieval and summarization, idea debate, hypothesis design, implementation, git-based versioning, validation, and retrospective closeout.

## Hard rules

1. Do not skip the hypothesis design stage before implementation.
2. Do not promote a method without explicit validation artifact.
3. Keep each stage artifact path explicit and auditable.
4. If critical guard checks fail, block chain completion.

## Operational References

Load when needed:
1. Load `references/chain-checklist.md` when checking required stage artifacts or deciding whether the chain can be considered complete.
2. Load `references/stage-flow.md` when you need the concrete stage order, delegated skill at each stage, or the required artifact path for a stage.
3. Load `references/milestone-reporting.md` when deciding whether a validated improvement is strong enough to justify milestone summary output.
