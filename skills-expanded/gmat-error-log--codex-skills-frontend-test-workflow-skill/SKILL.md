---
name: frontend-test-workflow
description: Orchestrates a complete frontend testing workflow by combining qa-test-planner (strategy) and frontend-testing (implementation). Use this when you need to rigorously test a component or feature from scratch.
---

# Frontend Test Workflow Skill

This skill orchestrates the end-to-end process of adding high-quality tests to the Bloom Mindful Companion frontend. It chains the strategic planning of `qa-test-planner` with the tactical implementation of `frontend-testing`.

## When to Use

Use this skill when:
- You need to add tests to a specific feature or component.
- You want to ensure tests cover edge cases and safety requirements (essential for mental health apps).
- You want a reliable, standardized process for testing.

## Workflow Steps

Follow these steps sequentially. Do not skip the planning phase.

### Phase 1: Strategy & Planning (`qa-test-planner`)

1.  **Analyze the Target**: Identify the component, hook, or flow to be tested.
2.  **Trigger `qa-test-planner`**: Explicitly ask the planner to "Create a test plan for [Target]".
    *   *Prompt*: "Using `qa-test-planner`, create a test plan for the `[Component/Feature]`."
3.  **Review the Plan**: Ensure the plan covers:
    *   **Happy Path**: Standard usage.
    *   **Edge Cases**: Empty states, errors, loading.
    *   **Safety/Privacy**: PII handling, verified outcomes.
    *   **Database State**: If applicable (Supabase integration).

### Phase 2: Implementation (`frontend-testing`)

1.  **Refactor for Testability** (If needed):
    *   Extract complex logic into pure utility functions (e.g., `src/utils/`).
    *   Ensure components are isolated or mockable.
2.  **Trigger `frontend-testing`**: Explicitly ask the testing skill to generate the code.
    *   *Prompt*: "Using `frontend-testing`, generate Vitest/RTL tests for `[Component]` following the test plan."
3.  **Incremental Creation**:
    *   Create `[Component].spec.tsx`.
    *   **DO NOT** generate all tests at once if complex. Start with rendering, then interaction.

### Phase 3: Verification & Execution

1.  **Run Tests**:
    *   Command: `npm test src/path/to/test.spec.tsx`
2.  **Fix & Iterate**:
    *   If tests fail, analyze the failure.
    *   Adjust code or test expectations.
3.  **Final Polish**:
    *   Ensure no lint errors in test files.
    *   Verify 100% pass rate for the target.

## Example Usage

> "Run the frontend-test-workflow for the `EmergencySOS` component."

**Agent Action**:
1.  Call `qa-test-planner` to list scenarios (Trigger: "Pressing SOS button", "Network failure during SOS").
2.  Call `frontend-testing` to write `EmergencySOS.spec.tsx`.
3.  Run `npm test` to verify.
