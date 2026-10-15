---
name: eng-spec
description: Freeze feature requirements into executable specifications (requirements, design contracts, task checklists) before any code is written. Use when a feature needs unambiguous contracts, when requirements drift must be prevented, or as the mandatory specification phase before eng-plan.
---

# Spec-Driven Development (SDD)

Freeze a feature's requirements into an executable, reviewable specification package before any planning or coding begins. The spec is the single source of truth; code is its byproduct.

> **Positioning**: This skill fills the specification layer between `prod-create-prd` (business vision) and `eng-plan` (implementation steps). It outputs contracts that downstream skills treat as immutable.

## Core Rules & Guardrails

- **Spec Before Code**: No implementation plan or code is produced until the spec package is frozen and confirmed by the user.
- **Single Source of Truth**: Once frozen, `specs/<feature>/` is immutable. Changes require an explicit re-freeze (version bump + changelog entry), never silent edits during implementation.
- **Executable & Testable Language**: Requirements are written as Given/When/Then behavioral clauses, not prose. Every requirement maps to at least one verifiable acceptance criterion.
- **Anti-Hallucination**: Every technical assumption (existing endpoints, data models, libraries) must be verified against the real codebase via tool inspection before being written into `design.md`.
- **Scope Discipline**: Out-of-scope items are explicitly listed. Anything not in the spec is not built.

---

## 3-Phase Specification Workflow

```
[Phase 1: Requirements Elicitation] ➔ [Phase 2: Design Contract Definition] ➔ [Phase 3: Freeze Gate & Sign-off]
```

### Phase 1: Requirements Elicitation (Briefing & Clarification Gate)
1. Ingest the user request and any existing PRD (`PRD.md`) or conversation context.
2. **Clarification Gate**: Formulate 3 to 5 blocker-level clarification questions for any behavioral ambiguity, conflicting requirements, or missing architectural decisions.
3. **Playback Brief**: Restate the clarified requirements as a concise Brief (Goals, Behavioral Clauses, Scope Boundaries, Non-Goals) and confirm with the user before defining contracts.
4. Extract user stories and formulate them as rigorous **Given/When/Then** clauses.
5. Enumerate in-scope and out-of-scope items explicitly.

### Phase 2: Design Contract Definition
1. **Interface Contracts**: Define API endpoints, request/response schemas, or function signatures.
2. **Data Models**: Define entities, fields, types, constraints, and relationships.
3. **State & Flow**: Define state machines or sequencing for stateful behavior.
4. **Verification**: Cross-check every contract against the existing codebase ,  reuse existing types, patterns, and conventions; never invent parallel ones.

### Phase 3: Freeze Gate
1. Self-check the spec package against the Quality Checklist below.
2. Present the spec to the user for explicit confirmation.
3. On confirmation, write the package to `specs/<feature-name>/` and mark it frozen.

---

## Spec Package Template

Write the following three files to `specs/<feature-name>/`:

### 1. `requirements.md`

```markdown
# Requirements: <feature-name>

## User Stories
### US-1: <title>
As a <role>, I want to <action>, so that <benefit>.

**Behavioral Clauses:**
- GIVEN <precondition> WHEN <action> THEN <outcome>
- GIVEN <precondition> WHEN <action> THEN <outcome>

## Acceptance Criteria
- [ ] AC-1: <verifiable criterion derived from US-1>
- [ ] AC-2: <verifiable criterion>

## Scope
- **In Scope**: <explicit list>
- **Out of Scope**: <explicit list ,  anything not listed in In Scope is not built>

## Open Questions (must be empty before freeze)
- None.
```

### 2. `design.md`

```markdown
# Design Contracts: <feature-name>

## Interface Contracts
| Endpoint / Function | Method | Request | Response | Error Cases |
|---|---|---|---|---|
| `/api/<resource>` | POST | `<schema>` | `<schema>` | 400 invalid, 401 unauthorized |

### Request Schema
```json
{ "field": "type ,  constraint" }
```

## Data Models
### <Entity>
| Field | Type | Required | Constraint | Description |
|---|---|---|---|---|
| `id` | string | yes | UUID v4 | Primary key |

## State Machine (if applicable)
| From | Event | To | Side Effect |
|---|---|---|---|
| `draft` | submit | `active` | emit notification |

## Codebase Alignment
- Existing types reused: `src/types/<file>.ext`
- Existing patterns mirrored: `src/<module>/<file>.ext`
```

### 3. `checklist.md`

```markdown
# Freeze Checklist: <feature-name>
- [ ] Every user story has at least one Given/When/Then clause.
- [ ] Every acceptance criterion is independently verifiable.
- [ ] In-scope / out-of-scope boundary is explicit.
- [ ] All interface contracts defined with error cases.
- [ ] All data models verified against existing codebase types.
- [ ] No open questions remain.
- [ ] User has explicitly confirmed the spec.
```

---

## Integration with Downstream Skills

- **`eng-plan`**: Detects `specs/<feature>/`; when present, treats it as the immutable input and derives tasks directly from acceptance criteria.
- **`eng-code-review`**: Performs spec conformance checks ,  verifying implementation satisfies the frozen acceptance criteria.
- **`eng-execute`**: Reports progress against AC identifiers (e.g. "AC-3 satisfied") rather than generic completion.

## Quality Gate Checklist

- [ ] Requirements written as Given/When/Then, not prose.
- [ ] Out-of-scope list is explicit and non-empty where ambiguity existed.
- [ ] Every contract references verified codebase artifacts.
- [ ] Freeze confirmed by the user before any planning begins.
---

## Checkable Completion Criteria

- [ ] `specs/<feature-name>/` contains requirements.md, design.md, and checklist.md.
- [ ] Requirements expressed as Given/When/Then with independently verifiable acceptance criteria.
- [ ] Interface contracts and data models verified against existing codebase types.
- [ ] Freeze explicitly confirmed by the user before downstream planning begins.
