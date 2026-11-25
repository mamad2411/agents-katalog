# Skill: Python Implementor
**Description**: Converts a Planned Python/Backend Slice into functional, verified code following TDD and architectural blueprints.
**Triggers**: `/py-implement [ID]`, "implement python backend slice", "start backend python implementation for [ID]", "code this slice in python"

## Instructions
When triggered, you MUST follow the Spec-Driven Development (SDD) protocol to move a slice from `Planned` to `In Review`.

### 1. Ingestion & Setup
* **State Verification**: Verify that the slice metadata (`.factory/slices/[ID].json`) is currently in **Phase: `planning`** and **Status: `Planned`**. If not, STOP and inform the user.
* **Immediate Transition**: Update metadata to **Status: `In Progress`** and **Phase: `implementation`** BEFORE starting any code work.
* **Branching (Mandatory)**: Create and switch to a dedicated feature branch: `factory/slice-[ID]`. DO NOT work in `main`. 
* **Context Load**: Read the target backend specifications:
    - Metadata: `.factory/slices/[ID].json`
    - Specification: `docs/specs/[ID].md` OR `docs/specs/product/[ID].md`
    - Plan: `.factory/slices/[ID]-PLAN.md`
    - Blueprint: `src/[ID]/interfaces.py` (if applicable)

### 2. Progress Tracking (Mandatory)
* **Metadata Heartbeat**: Every 3 minutes (or at every major logic block), update the `updated_at` field in the slice metadata and commit the change to the feature branch. This ensures the dashboard reflects live backend progress.

### 3. TDD Execution (Mandatory)
For every functional unit defined in the blueprint and plan:
1. **Define Test**: Create or update a test file in `tests/[ID]/test_[module].py`.
2. **Execute Test (Fail)**: Run the test to confirm it fails (Red phase).
3. **Implement Code**: Move the relevant logic to its permanent home in `src/` and provide the implementation.
4. **Execute Test (Pass)**: Run the test again to confirm it passes (Green phase).
5. **No Refactor Rule**: Once the test passes, **do not refactor**. Move immediately to the next unit. Optimization is a separate stage in the Factory pipeline.

### 4. Verification & Compliance
* **Edge Cases**: Ensure tests cover boundary conditions, null inputs, and error states.
* **Contract Validation**: Ensure the final implementation respects all schemas in `.factory/contracts/` (e.g., `aggregate_slice_info.json`).
* **Lint & Type Check**: Run project-standard tools (`mypy`, `ruff`) if available in the environment to ensure quality.

### 5. Finalization & Reporting
* **Completion Transition**: 
    - Change status to **`In Review`** and Phase to **`validation`** in `.factory/slices/[ID].json`.
    - Update `updated_at` timestamp.
* **PR Readiness**: Prepare a summary of changes for the human reviewer including the location of the final source and test files.
* **Telemetry**: Conclude the session with the mandatory reporting block.

**TERMINAL INSTRUCTION**: "Python Implementation complete for [ID]. Tests passed, branch pushed, and metadata updated to 'In Review / validation'. Ready for PR validation."