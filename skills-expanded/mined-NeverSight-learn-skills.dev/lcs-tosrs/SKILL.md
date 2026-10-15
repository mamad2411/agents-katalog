---
name: lcs-tosrs
description: Use this skill whenever user asks to transform PRD into SRS, implementation specification, deterministic requirements, acceptance criteria mapping, or AI-ready engineering contract. Trigger on phrases like "create SRS", "PRD to SRS", "spec from PRD", "make requirements testable", or "generate implementation-ready spec".
adapters: [claudecode, opencode]
compatibility: [claudecode, opencode]
---

LCS ToSRS Skill

Shared Coding Contract
- Refer to Shared Coding Workflow Contract in `../lcs-shared/contract.md` for folder conventions, Handoff format, and token optimization.

Purpose
- Transform `prd.md` into deterministic Lean SRS artifacts optimized for AI implementation and QA.
- Reduce ambiguity, hallucination, and inconsistent implementation.
- Keep output lightweight, markdown-first, traceable, and implementation-ready.

Trigger
- Activate when user requests PRD-to-SRS transformation, implementation specification, requirement traceability, acceptance criteria normalization, or deterministic engineering contract.

Do not overlap with other skills
- Do not generate granular execution files `task/task-###.md`.
- If user asks to slice execution tasks, handoff to `lcs-task-slicer`.
- `lcs-tosrs` owns: `srs.md`, `tests.md`, optional `api.md`, optional `db.md`.

Input and output location
- Work item folder: `.lcs/work-items/<YYYYMMDD-HHMMSS>-<slug-work-item>/`
- Preserve existing `prd.md`.
- Generate or overwrite:
  - `srs.md` (required)
  - `tests.md` (required)
  - `api.md` (optional, only when API changes are relevant)
  - `db.md` (optional, only when DB changes are relevant)

Behavior checklist
1. Read `.lcs/state.md` first when continuing existing work.
2. Locate active work-item folder and `prd.md`.
3. Extract from PRD:
   - features
   - business goals
   - user roles
   - business rules
4. Generate deterministic requirement sets:
   - functional requirements
   - validation rules
   - edge cases
   - acceptance criteria
5. Draft API contract details when API behavior exists.
6. Draft DB impact details when schema/persistence changes exist.
7. Build traceability mapping across requirement families and tests.
8. Produce stable markdown output with repeated structure.

Requirement design rules
- Every requirement must be atomic, deterministic, testable, and implementation-oriented.
- Avoid vague words like "properly", "fast enough", "secure enough".
- Use measurable and verifiable statements.

ID policy (mandatory)
- Use 3-digit sequential IDs per category:
  - `FR-001`
  - `BR-001`
  - `VR-001`
  - `EC-001`
  - `API-001`
  - `DB-001`
  - `AC-001`
  - `TEST-001`
- Keep numbering stable and deterministic in regeneration.

Deterministic regeneration rules
- Overwrite target file content, do not append ad-hoc sections.
- Keep heading order fixed.
- Keep template shape fixed.
- Keep wording concise and implementation-focused.

SRS.md required structure

# Work Item Overview

# System Overview

# User Roles

# Functional Requirements

# Business Rules

# Validation Rules

# Edge Cases

# Non Functional Requirements

# API Contracts

# Database Impact

# Acceptance Criteria

# Requirement Traceability

Functional requirement template (exact)
```md
## FR-001 <Requirement Name>

### Description
Short deterministic description.

### Inputs
- input_1
- input_2

### Process
1. Step one
2. Step two
3. Step three

### Outputs
- output_1
- output_2

### Validation
- rule_1
- rule_2

### Edge Cases
- edge_case_1
- edge_case_2

### Acceptance Criteria
- AC-001
- AC-002
```

Business rule template
```md
## BR-001 <Rule Name>

Description:
Explicit business constraint.

Impact:
Affected features/modules.
```

Validation rule template
```md
## VR-001 <Validation Name>

Condition:
Validation condition.

Error Response:
Expected rejection behavior.
```

Edge case template
```md
## EC-001 <Edge Case Name>

Scenario:
Failure or unexpected scenario.

Expected Behavior:
How system must respond.
```

Acceptance criteria template
```md
## AC-001 <Acceptance Name>

Given:
<precondition>

When:
<action>

Then:
<expected result>
```

NFR template
```md
## Performance
- API response under 300ms for P95 baseline.
- Support defined concurrent load target from PRD.

## Security
- Authentication and authorization constraints are explicit.
- Sensitive endpoints have abuse controls (for example rate limiting).

## Reliability
- Error handling path defined for all critical flows.
- Retries/idempotency rules defined where relevant.

## Scalability
- Scale constraints and bottleneck assumptions are explicit.
- Horizontal/vertical scaling expectation is stated.
```

API contract template (for srs.md and/or api.md)
````md
## API-001 <Endpoint Name>

Method:
POST

Route:
/api/example

Request:
```json
{
  "field": "string"
}
```

Response:
```json
{
  "result": "string"
}
```

Errors:
- error_code_1
- error_code_2
````

DB impact template (for srs.md and/or db.md)
```md
## DB-001 <Table Name>

| field | type | notes |
|---|---|---|
| id | bigint | primary key |
| created_at | timestamp | |
```

tests.md required content
- Test scenarios grouped by feature/module.
- Coverage matrix mapping `TEST-###` to related IDs.
- Each test must include:
  - Covers
  - Type
  - Preconditions
  - Steps
  - Expected

tests.md template
```md
# Test Plan

## Coverage Matrix

| Test ID | Covers | Type | Priority |
|---|---|---|---|
| TEST-001 | AC-001, FR-001 | integration | P0 |

## <Feature Name>

### TEST-001 <Test Name>

Covers:
- AC-001
- FR-001

Type:
- integration

Preconditions:
- precondition_1

Steps:
1. step_1
2. step_2

Expected:
- expected_1
- expected_2
```

Traceability rules
- Every FR must map to at least one AC.
- Every AC must map to at least one TEST.
- Requirement Traceability section must include cross-reference matrix:
  - FR -> BR/VR/EC/API/DB/AC/TEST

Writing style
- Concise.
- Structured.
- Technical.
- Repetitive section pattern.
- Minimal prose.
- Markdown-only.

Handoff (mandatory footer in every generated artifact)
```md
## Handoff

Next recommended skill: lcs-task-slicer
Next file to read: .lcs/work-items/<YYYYMMDD-HHMMSS>-<slug-work-item>/srs.md
Current phase: tasks
Current confidence: <low/medium/high>
Blocking questions: <list or None>
Risks to carry forward: <short>
Suggested next command: Slice srs.md into task/task-###.md with strict requirement references
```
