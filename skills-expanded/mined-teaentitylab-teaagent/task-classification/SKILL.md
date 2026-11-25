---
name: task-classification
description: Classify a coding task by type and complexity and generate a structured multi-step workflow plan. Owns the reviewed LLM prompt templates for the coordinator's classification and planning paths.
---

# Task Classification & Workflow Planning

Reviewed prompt assets for the task-coordination reasoning in
`teaagent.domain.coordinator` (ADR-0041 Phase 2, behavior-preserving thinning).
The deterministic heuristic classifier/planner stays in the harness as the
default and as the fallback when no LLM adapter is configured; these assets own
the **LLM-path** prompt text so the prompt reasoning is a reviewed supply-chain
asset rather than inline Python.

## Assets

- `classification_prompt.md` — user prompt for classifying a task into
  `task_type` / `complexity` / confidence / routing (JSON response).
  Placeholder: `{task_description}`.
- `planning_prompt.md` — user prompt for generating a structured multi-step
  workflow plan (JSON response). Placeholders: `{task_description}`,
  `{task_type}`, `{complexity}`, `{estimated_steps}`, `{available_agents}`.

## Procedure

1. Classify the task type (`code_review`, `testing`, `documentation`,
   `refactoring`, `debugging`, `feature_implementation`, `general`) and
   complexity (`simple`, `moderate`, `complex`); estimate whether it needs
   multiple steps.
2. For multi-step tasks, generate an ordered list of steps — each naming an
   agent and its tools, with dependencies.
3. Always respond with valid JSON in the schema the prompt specifies.

## Contract

`TaskCoordinator` loads these templates via
`teaagent.domain._prompt_assets.load_prompt_template` and `str.format(...)`s them
with runtime values. The rendered prompt is byte-identical to the prior inline
prompt (locked by `tests/domain/test_prompt_assets.py`). If an asset is missing,
the coordinator degrades to its deterministic heuristic — the same path taken
when no LLM adapter is available.
