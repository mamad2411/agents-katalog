---
name: qa-story-analysis
description: 'Expert software testing engineer workflow for Jira story analysis and test scenario design. Use when users ask to analyze stories, acceptance criteria, and requirements, identify coverage and risks, and produce scenario outputs ready for downstream test case generation.'
argument-hint: 'Provide a Jira story key (e.g. TSPCM-5745) or paste the story content'
---

# QA Story Analysis and Scenario Design

Analyze a user story like a senior QA engineer and produce structured test scenarios that can be consumed directly by a test case generation skill.

## Use When

- User asks to analyze a Jira story, ticket, PRD excerpt, or acceptance criteria
- User asks what to test, test coverage, edge cases, or risk-based scenarios
- Output must be ready for detailed test case generation

## Inputs

Collect these inputs before scenario design:

- Story metadata: story key, title, type, status, priority, story points
- Description and acceptance criteria
- Linked issues, epic context, and comments
- Business constraints, technical constraints, and environment hints

If any required input is missing, record it under `Clarifications Needed`.

## Workflow

### Phase 1: Story Decomposition

1. Extract and normalize:
- Persona/actor
- Goal/action
- Business value
- Rules/constraints
- Explicit acceptance criteria (`AC-1`, `AC-2`, ...)

2. Add inferred requirements where needed:
- Label each as `[Inferred]`
- Keep inferred requirements minimal and justified

### Phase 2: Risk and Scope Assessment

Classify and justify:

- Complexity: Low, Medium, High
- Risk: Low, Medium, High, Critical
- Primary test layers: UI, API, integration, data, security, accessibility, performance
- Dependency risk: external systems, jobs, feature flags, timing windows

### Phase 3: Unclear Areas and Clarifications

Identify any ambiguities or missing information that would prevent `TC-Ready: Yes` scenarios. For each, create a concise clarification question to ask the user:
  - Create a numbered list of clarification questions.
  - Each question should be specific and directly tied to enabling scenario design.
  - Example: "AC-2 states 'user receives notification' - is this an email, in-app message, or both?"


### Phase 4: Scenario Design

Generate scenarios using this exact structure:

```text
[TS-###]
Category: <Happy Path | Alternate Happy Path | Negative | Boundary | Edge Case | Integration | Non-Functional>
Title: <Short action-focused title>
Priority: <P0 | P1 | P2 | P3>
Preconditions: <required setup state>
Input/Action: <user/system action>
Expected Result: <observable expected behavior>
Test Data Hint: <concrete data guidance>
Linked AC: <AC-# | Inferred>
TC-Ready: <Yes | Needs Clarification>
```

Minimum coverage set:

- 1 primary happy path
- Alternate valid paths
- Negative/error handling paths
- Boundary conditions (date, amount, state transitions)
- Edge cases (ordering, stale state, concurrency if relevant)
- Integration interactions (upstream/downstream effects)
- Non-functional scenarios when risk is Medium+

### Phase 5: Acceptance Coverage Matrix

Create a traceability table:

```text
| Acceptance Criterion | Scenario IDs | Coverage |
|---|---|---|
| AC-1 ... | TS-001, TS-003 | Covered |
| AC-2 ... | TS-004 | Partial |
| AC-3 ... | - | Gap |
| [Inferred] ... | TS-007 | Inferred |
```

Mark every uncovered AC as `Gap`.

### Phase 6: Test Case Generation Handoff

End with:

```text
## TC GENERATION HANDOFF
Story ID: <...>
Scenario Count: <...>
Priority Breakdown: P0=<n>, P1=<n>, P2=<n>, P3=<n>
Coverage Gaps: <None or list>
Clarifications Needed: <None or numbered list>
Suggested Data Sets: <specific accounts/data combinations>
Automation Candidate: <Yes | Partial | No> with one-line rationale
```

## Quality Gates

Before final output, ensure:

- Each acceptance criterion maps to at least one scenario or is explicitly marked as a gap
- Scenario titles are concise and non-duplicative
- Expected results are observable and testable
- Scenario set is prioritized by business impact and risk
- Output is ready for direct consumption by a test case generator (no procedural ambiguity)
- Read discussion and comments for additional context that may inform scenario design, or get the final updates from the story if it is still being refined, to ensure the most accurate and comprehensive scenarios possible.
- If any critical information is missing that prevents scenario design, list it under `Clarifications Needed` and mark affected scenarios as `TC-Ready: Needs Clarification`.

## Constraints

- Do not generate detailed test case steps in this skill
- Do not assume hidden behavior without labeling it as `[Inferred]`
- Ask concise clarification questions only when a scenario cannot be made `TC-Ready: Yes`
