---
name: follow-deep
description: Consider and invoke the relevant deep-* workflows based on the task context
argument-hint: "[scope]"
related:
  - review
  - deep-review-codebase
  - deep-analyze
  - plan
  - refactor
  - deep-validate
  - follow-parallel

---

## Goal

Consider and invoke the relevant `deep-*` workflows based on the task context, so the work reaches depth across every dimension

## Scope

Use as a sub-workflow to decide which `deep-*` workflows the current task should call — it is not a standalone main workflow

See also: /deep-review-codebase

## Execute

### 1. Identify Task Context

> Goal: identify the current task context to decide which deep- workflows are relevant

1. Classify the task type: analyze, review, plan, refactor, test, validate, secure, optimize, research
2. Classify the complexity: low, medium, high
3. Classify the risk level: low, medium, high
4. If the task is simple or low risk → no deep- workflows needed

### 2. Select Deep Workflows

> Goal: pick the deep- workflows relevant to the task context

1. Analysis → `deep-analyze` (includes scripts/review CLI)
2. Review → `deep-review-codebase` (comprehensive) or `/review-*` (specific dimension)
3. Planning → `plan`
4. Refactoring → `refactor`
5. Testing → `run-test`
6. Validation → `deep-validate`
7. Security → `deep-review-codebase`
8. Performance → `/deep-review-codebase` (comprehensive) or `deep-review-codebase` (specific)
9. Research → `deep-research` (multi-source) or `learn-from-web` (single-source)
10. Thinking → `deep-thinking` (systematic) or `deep-thinking` (reflective)

### 3. Execute Selected Workflows

> Goal: follow the selected deep- workflows, using parallel execution when possible

1. If several workflows are selected and they are independent → use `follow-parallel` for parallel execution
2. If several workflows are selected and they have dependencies → run them in order
3. If a single workflow is selected → run it directly
4. Record the results from each workflow

### 4. Apply Deep Follow If Needed

> Goal: if the task needs recursive follow-through, use `follow-deep`

1. If the selected deep- workflows have complex sub-workflows → run `follow-deep`
2. If the selected deep- workflows are straightforward → no need for `follow-deep`
3. Record the summarized results

## Rules

### 1. When To Use Deep Workflows

- Use `deep-*` workflows when the task is highly complex or high risk
- Do not use `deep-*` workflows for simple tasks that can be done directly
- If unsure → run `deep-thinking` to consider before choosing

### 2. Selection Criteria

- Select only the deep- workflows genuinely relevant to the task
- Do not always call every deep- workflow — choose based on context
- If the task is about review → use `deep-review-codebase`, not `deep-analyze`
- If the task is about analysis needing scripts → use `deep-analyze` (scripts/review CLI already merged into it)

### 3. Parallel Execution

- If several independent deep- workflows are selected → use `follow-parallel`
- Limit parallel operations to at most 10 per batch
- If deep- workflows have dependencies → run them in order

### 4. Deep Follow Integration

- Use `follow-deep` when deep- workflows have complex sub-workflows
- Do not use `follow-deep` for straightforward deep- workflows
- `follow-deep` supports recursive traversal of both workflows and skills

## Expected Outcome

- The relevant deep- workflows are selected and executed efficiently
- Unnecessary deep- workflows are not invoked
- Independent deep- workflows run in parallel, reducing total execution time
- Results from the deep- workflows are recorded and summarized

