---
name: orchestration-plan
description: "Gemini adapter for /plan. Converts approved design+review artifacts into implementation-ready, conflict-free task groups with explicit verification."
---

# /plan - Deterministic Execution Plan (Gemini Adapter)

## Use this when
- `/ar` output is approved.
- The user requests `/plan`, implementation planning, or task decomposition.

## Model tier
Use a balanced-reasoning model. Task decomposition is systematic and bounded; full high-reasoning is not required.

## Semantic intent
- Predeclared verification: define tests and acceptance checks before coding starts.
- Context minimization: task groups should be specific enough that builders do not need extra narrative.

## Input
- `.pipeline/runs/<run-id>/design.json`
- `.pipeline/runs/<run-id>/review.json`

## Procedure

### 1. Build task groups
Partition work into independent groups (target 3-6 tasks/group, max 8).
If a group falls outside 3-6 tasks, add `scope_override.reason` in that group and justify why.
Assign `builder_tier` per group: `high_reasoning` for groups requiring architectural judgment or complex refactoring, `balanced` for structured implementation with reasoning, `fast` for straightforward implementation tasks.

### 2. Assign file ownership
Create explicit path->group mapping and remove overlaps.

### 3. Provide executable code patterns
For each task, include concrete patterns (imports/signatures/structure), not placeholders.

### 4. Define tests upfront
Each task needs named test cases containing:
- setup,
- assertion,
- expected outcome.

### 5. Define acceptance criteria
Attach non-negotiable completion checks per task.

### 6. Define verification commands
Include exact commands for lint/format-check/type/build/test checks.

### 7. Run pre-final drift check
Compare plan against design (via `/pmatch` flow or `multi-model-review` drift mode).
Resolve structural drift before finalizing.

### 8. Build artifact
Write `plan.json` conforming to `contracts/artifacts/execution-plan.schema.json`:
- `.pipeline/runs/<run-id>/plan.json`

### 9. Gate evaluation
Validate:
- schema compliance,
- at least one test case per task,
- file ownership conflicts absent,
- no TODO/placeholders in required code patterns,
- verification command list present,
- task-group granularity in 3-6 range unless `scope_override.reason` is provided.

Write gate output to:
- `.pipeline/runs/<run-id>/gates/plan-gate.json`

## Non-negotiables
- If builders must infer missing intent, planning is incomplete
- No placeholder implementation guidance
- Test design happens before build, not after
