---
name: plan-fix
description: Produce a detailed, reviewable implementation plan for a confirmed bug before any code is written.
user-invocable: true
---

# /plan-fix — Implementation Planning

You are an AI assistant creating a detailed implementation plan for a confirmed bug fix. Follow the procedure below precisely.

## Step 0: Load Context

1. The workspace may contain multiple repositories, each with its own `agents.md` at its root. Identify the relevant repository and read its `agents.md`. If it doesn't exist, stop and tell the developer to create one (point them to `agents.md.template`). Verify it contains **Architecture**, **Feature Inventory**, and **Testing** sections. If any are missing, stop and report what's needed.
2. Read `.ai/issue-analysis.md`. If it doesn't exist, tell the developer to run `/reproduce` first.
3. Verify the issue is classified as a **Bug** in the analysis. If not, stop.

## Step 1: Map the Affected Code

Using `agents.md > Architecture`:
1. Identify the exact modules, classes, and methods involved.
2. Read the source code for these components.
3. Trace the execution path from entry point to the point of failure.

## Step 2: Identify the Fix

Determine the **minimal** code change that addresses the root cause.
- Prefer fixes that align with existing patterns in the codebase (refer to `agents.md > Key Abstractions & Patterns`).
- Do not refactor or reorganize code beyond what is needed to fix the bug.

## Step 3: Assess Blast Radius

List all components and features that could be affected by this change. Cross-reference with `agents.md > Feature Inventory`.

## Step 4: Clarify Ambiguities

If there are multiple valid approaches, or if the fix might change observable behavior beyond the bug, **stop and ask the developer** before proceeding. Present the trade-offs clearly.

## Step 5: Design the Test Plan

Before designing tests, read and follow the project's testing conventions from `agents.md`:

1. **Determine the test framework:** Check `agents.md > Testing > Test Framework & Conventions` for which frameworks the project uses (e.g., JUnit, pytest, Jest, Mocha, etc.). All new tests **must** use the same framework — do not introduce a different one.

2. **Follow naming conventions:** Use the test naming pattern defined in `agents.md > Testing > Test Framework & Conventions` (e.g., `testMethodName_scenario_expectedResult`, or whatever the project convention is). Look at existing tests near the affected code for concrete examples.

3. **Place tests in the correct location:** Use `agents.md > Testing > Test Framework & Conventions` to determine where tests live relative to source code (e.g., `src/test/` mirroring the source structure, a `tests/` directory, or a separate test module). Unit tests and integration tests may live in different directories or modules — follow what the project already does.

4. **Use project test infrastructure:** Check `agents.md > Testing > Test Infrastructure` for available test containers, mock services, base test classes, test utilities, or fixtures. Reuse existing helpers rather than creating new ones.

5. **Determine test commands:** Reference `agents.md > Testing > Running Tests` so the implementation plan includes the exact commands to run the new tests and the affected module's existing test suite.

Now specify the exact tests to write:
- What each test asserts
- Which category (unit/integration) and why
- The file path where it lives (following the project's directory structure)
- The test framework and base class to use
- Any test infrastructure dependencies (containers, mock services, fixtures)
- Include negative and boundary cases
- The command to run each test individually and as part of the suite

## Step 6: Document Breaking Changes

If the fix changes any public API, config format, wire protocol, or default behavior, explicitly flag it.

## Step 7: Write the Output Artifact

Write the plan to `.ai/implementation-plan.md` using this exact format:

```markdown
# Implementation Plan — [Issue #ID]: [Issue Title]

## Summary
One-paragraph description of what will be changed and why.

## Root Cause (Confirmed)
[Refined from issue-analysis.md after code inspection]

## Implementation Details

### Files to Modify
| File | Change Description | Rationale |
|------|--------------------|-----------|
| path/to/file | [what changes] | [why this specific change] |
| ... | ... | ... |

### Implementation Steps
1. [Ordered steps the AI will follow during /implement]
2. ...

### Code Approach
[Pseudocode or detailed description of the logic change.
Reference existing patterns from the codebase.]

## Test Plan

### Testing Conventions (from agents.md)
- **Framework:** [as specified in agents.md, e.g., JUnit, pytest, Jest, etc.]
- **Naming pattern:** [e.g., testMethodName_scenario_expectedResult]
- **Base class / utilities:** [any project base test class or test helpers to extend/use]
- **Test infrastructure:** [containers, mock services, or fixtures needed]

### New Tests
| Test Name | Type | Asserts | Location | Run Command |
|-----------|------|---------|----------|-------------|
| test_x_returns_y_when_z | Unit | [assertion] | path/to/test_file | [command] |
| test_x_fails_gracefully_on_invalid_input | Unit | [assertion] | path/to/test_file | [command] |
| test_end_to_end_flow_with_fix | Integration | [assertion] | path/to/test_file | [command] |

### Existing Tests to Run
[List of existing test classes/suites that must pass after the change, with the exact commands from agents.md > Testing > Running Tests]

## Impact Assessment
- **Affected components:** [list]
- **Affected features:** [list]
- **Breaking changes:** None / [describe what breaks and migration path]
- **Performance implications:** None / [describe]
- **Security implications:** None / [describe]

## Open Questions
[Any unresolved ambiguities — these block /implement until answered]
```

## Important Rules

- **Never guess.** If you encounter ambiguity, stop and ask the developer.
- **Minimal blast radius.** Changes must be scoped to the smallest set of files that fix the issue. Resist broad refactors.
- **Artifacts over memory.** The plan must be complete enough for a different agent to implement it.
- After writing the artifact, inform the developer to review the plan. If `Open Questions` is non-empty, those must be answered before proceeding. The plan should then go through `/review-plan`.
