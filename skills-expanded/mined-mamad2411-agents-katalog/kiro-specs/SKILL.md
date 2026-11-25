---
name: kiro-specs
description: Kiro-style spec-driven development workflow for AI agents. Creates structured specifications (requirements.md, design.md, tasks.md) using EARS notation, property-based testing, and three-phase workflows. Use when building complex features, fixing critical bugs, or when structured planning and documentation are needed before implementation.
---

# Kiro Specs — Spec-Driven Development

## On Invocation

When this skill loads, follow these steps in order:

1. **Clarify intent** — If not already clear from context, ask:
   - What are we building or fixing?
   - Is this a new feature or a bug fix?
   - For features: Do you have a behavior in mind (Requirements-First) or an architecture in mind (Design-First)?
   - For Design-First: Do you want **High Level Design** (system architecture, component interactions, diagrams) or **Low Level Design** (pseudocode, algorithms, interface definitions)?
   - For bugs: Collect all 4 elements — reproduction steps, current behavior, expected behavior, and constraints on unchanged code
   - Do you have existing designs, diagrams, or requirements to import? (e.g., architecture docs, JIRA tickets, Confluence pages, PNG diagrams)

2. **Explore the codebase** — Before writing any spec, read relevant files to understand:
   - Existing architecture, patterns, and conventions
   - Related components that will be affected
   - Test patterns and frameworks used in the project
   - Skip this step only if there is no codebase (greenfield project)

3. **Determine the spec directory** — Use `.kiro/specs/[kebab-case-feature-name]/` as the output path.

4. **Execute phases with approval gates** — Complete one phase, show the user the output, and **wait for explicit approval** before moving to the next phase. Do not auto-advance.

5. **Write files to disk** — Use the Write tool to create actual files. Don't just show the content in chat.

---

## When to Use Specs vs Quick Coding

**Use specs when:**
- Building complex features requiring structured planning
- Fixing bugs where regressions are costly or root cause is unclear
- Previous fix attempts have caused regressions
- Requirements or design need iteration before code is written
- Multiple discrete implementation tasks are involved
- Documentation is needed for team collaboration or compliance

**Use quick coding (chat) when:**
- Quick exploratory coding or prototyping
- Simple one-liner fixes, typo corrections, or obvious logic errors
- The full scope is obvious and small
- No regression risk from the change

---

## Spec Types

### Feature Spec

Three files: `requirements.md` → `design.md` → `tasks.md`

#### Workflow Variants

**Requirements-First** (Behavior → Architecture → Tasks)
- Use when: behavior is known, architecture is flexible, product-driven development, greenfield projects
- Phase 1: Write `requirements.md` with EARS notation
- Phase 2: Derive `design.md` from requirements
- Phase 3: Generate `tasks.md` with property-based test properties

**Design-First** (Architecture → Requirements → Tasks)
- Use when: architecture is decided, porting existing design docs, strict non-functional constraints, exploring technical feasibility
- Choose a detail level:
  - **High Level Design** — Full architecture: system diagrams, component interactions, technology stack, non-functional properties. Best for complex systems, team collaboration, thorough documentation.
  - **Low Level Design** — Implementation focus: pseudocode, algorithms, interface definitions, key data structures. Best for rapid prototyping, quick feasibility checks, solo development.
- Phase 1: Write `design.md` (at chosen detail level)
- Phase 2: Derive `requirements.md` from design — requirements are guaranteed feasible since they come from a validated architecture
- Phase 3: Generate `tasks.md` with property-based test properties

**Importing Existing Work:**
- Existing designs/architecture docs can be pasted or referenced as input for Design-First Phase 1
- Existing requirements from JIRA/Confluence/etc. can be imported and formalized into EARS notation for Requirements-First Phase 1
- PNG/image diagrams can be described and incorporated into `design.md`

### Bugfix Spec

Three files: `bugfix.md` → `design.md` → `tasks.md`

- Phase 1: Write `bugfix.md` — collect all 4 elements: reproduction steps, current (defective) behavior, expected behavior, and unchanged behaviors to preserve
- Phase 2: Write `design.md` — root cause analysis, fix approach, property-based test properties, risk assessment
- Phase 3: Write `tasks.md` — implementation steps with regression-prevention tests

---

## EARS Notation (Requirements Language)

Use EARS patterns for every requirement. Choose the pattern that fits the condition type:

| Pattern | Syntax | Use for |
|---------|--------|---------|
| Event-driven | `WHEN [event] THE SYSTEM SHALL [behavior]` | Triggered actions |
| State-driven | `WHILE [state] THE SYSTEM SHALL [behavior]` | Continuous behaviors |
| Conditional | `IF [condition] THEN THE SYSTEM SHALL [behavior]` | Unwanted/error cases |
| Ubiquitous | `THE SYSTEM SHALL [behavior]` | Always-true invariants |
| Optional feature | `WHERE [feature is enabled] THE SYSTEM SHALL [behavior]` | Feature flags |
| Compound | `WHILE [state] WHEN [event] THE SYSTEM SHALL [behavior]` | State + trigger |

**Examples:**
```
WHEN a user submits a form with invalid data THE SYSTEM SHALL display inline validation errors
WHILE a background sync is in progress THE SYSTEM SHALL show a loading indicator
IF authentication fails three consecutive times THEN THE SYSTEM SHALL lock the account for 15 minutes
THE SYSTEM SHALL encrypt all passwords using bcrypt with cost factor ≥ 12
WHERE the beta feature flag is enabled WHEN a user visits the dashboard THE SYSTEM SHALL show the new UI
```

**Benefits:** Clarity, testability, traceability, completeness — each requirement maps directly to a test case.

---

## Property-Based Testing (PBT) Integration

Property-Based Testing validates universal properties across entire input spaces, not just individual examples. PBT is integrated throughout the spec workflow.

### What is a Property?

A property is a universal statement about system behavior — an invariant or contract that should always hold, regardless of specific data. Each EARS requirement naturally maps to a property.

**Traditional test:** "User adds car X to favorites → car X appears in list"
**Property:** "For ANY user and ANY car, WHEN added to favorites, the system displays it in the user's list"

PBT tests hundreds of combinations automatically, using "shrinking" to find minimal counter-examples.

### PBT Workflow

```
EARS Requirements → Extract Properties → Add to tasks.md → Run tests → Identify failures → Fix & validate
```

1. **Design Phase**: Extract testable properties from EARS-formatted requirements. Each property links back to its source requirement (REQ-N.M).
2. **Tasks Phase**: Include property-based test tasks. PBT tasks are optional by default but recommended.
3. **Execution**: Run generated PBT cases against implementations. When tests fail, identify specific failure scenarios for debugging.

### PBT in Bugfix Specs

For bugfix specs, properties validate three things:
- **Bug exists**: Current implementation produces incorrect behavior (test fails before fix)
- **Fix works**: Fixed implementation produces correct behavior (test passes after fix)
- **No regressions**: Unchanged behaviors still hold (existing tests still pass)

---

## File Structures

See `templates/spec-templates.md` for complete copy-paste templates.

### requirements.md
```
# Feature: [Name]
## Overview
## User Stories
  ### Story N: [Title]
  As a [role], I want [capability], so that [benefit].
  #### Requirements (EARS notation, REQ-N.M IDs)
  #### Acceptance Criteria (Given/When/Then)
## Non-Functional Requirements
## Out of Scope
## Dependencies
```

### design.md (Feature)
```
# Design: [Name]
## Architecture Overview
## Component Design (Purpose, Responsibilities, Interfaces, Dependencies)
## Sequence Diagrams (mermaid: main flow + error flow)
## Data Model (entities, schema changes, migrations)
## API Design (endpoints table, request/response examples)
## Error Handling (table: scenario → status → code → message)
## Security Considerations
## Testing Strategy (unit, integration, e2e, performance)
## Implementation Considerations (trade-offs, alternatives, risks)
```

### tasks.md
```
# Tasks: [Name]
## Summary table (# | Task | Status | Required)
  Status values: [ ] pending, [~] in-progress, [x] done
## Task Details (Description, Files, Acceptance criteria, Dependencies)
## Execution Order
```

### bugfix.md
```
# Bugfix: [Title]
## Bug Analysis
  ### Current Behavior (Defect) — WHEN/THEN
  ### Expected Behavior — WHEN/THEN SHALL
  ### Unchanged Behavior — WHEN/THEN SHALL CONTINUE TO
## Reproduction Steps
## Impact Assessment (Severity, Affected, Frequency, Workaround)
## Environment
```

### design.md (Bugfix)
```
# Design: Bugfix for [Title]
## Root Cause Analysis
## Proposed Fix
## Properties to Test (bug exists / fix works / no regressions)
## Files to Modify
## Risk Assessment (level, side effects, mitigation)
```

---

## Phase Execution

### Phase Approval Gate

After writing each phase file:
1. Show the user the file path and a brief summary of key decisions
2. Ask: "Does this look right? Any changes before I move to the next phase?"
3. Wait for explicit go-ahead before proceeding

### Task Execution

**Sequential mode** — Execute tasks one at a time:

```
For each task:
  1. Update tasks.md: mark status [~] (in-progress)
  2. Implement the task (read relevant files first)
  3. Write/run tests (including PBT if applicable)
  4. Update tasks.md: mark status [x] (complete)
  5. Report completion before moving to next task
```

**Batch mode** — Run all required tasks at once when the user requests it. Execute in dependency order, skip optional tasks unless explicitly included. Update tasks.md status in real-time.

Use TodoWrite to track task progress in the current session when executing multiple tasks.

---

## Spec Organization

```
.kiro/specs/
├── user-authentication/
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
├── checkout-flow/
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
└── payment-bug-2026-04/
    ├── bugfix.md
    ├── design.md
    └── tasks.md
```

**Conventions:**
- One spec per feature or bug — no monolithic specs
- Version control specs alongside code
- Spec directory name = kebab-case feature identifier
- Include date in bugfix directory names for traceability

---

## Updating Existing Specs (Refinement Cascade)

When any spec file changes, downstream files must be updated to stay consistent. Follow this cascade:

**Requirements changed → Refine design → Refine tasks:**
1. Read the updated `requirements.md`
2. Identify which sections of `design.md` are affected by the change
3. Regenerate affected `design.md` sections (preserve unaffected sections)
4. Regenerate affected `tasks.md` entries
5. Show a diff summary of all changes before writing

**Design changed → Validate requirements → Refine tasks:**
1. Read the updated `design.md`
2. Validate that all requirements in `requirements.md` are still feasible — flag any that aren't
3. Re-derive affected requirements if needed
4. Regenerate affected `tasks.md` entries
5. Show a diff summary before writing

**Check task progress:**
- Read the codebase and compare against task acceptance criteria
- Update `tasks.md` to mark already-implemented tasks as `[x]`
- Useful when resuming work or onboarding to an existing spec

**Always** read the current file before writing an updated version — avoid overwriting user edits without confirmation.

---

## Quality Gates

| Gate | Requirement |
|------|-------------|
| Requirements complete | All EARS requirements use correct pattern, no ambiguous SHALL |
| Design complete | Sequence diagrams cover main + error flows, all components documented |
| Properties extracted | Each EARS requirement has a corresponding testable property |
| Tasks defined | Each task has specific acceptance criteria and file list |
| Implementation | All required tasks `[x]`, tests passing |
| PBT validation | Property-based tests pass for key requirements (when applicable) |
| Spec compliance | Implementation matches all documented REQ-N.M requirements |

---

## Multi-Spec Projects

A repository can contain unlimited specs organized by feature. Each spec is independent — teams can work on different specs without conflicts.

```
.kiro/specs/
├── user-authentication/    ← Team A
├── product-catalog/        ← Team B
├── shopping-cart/          ← Team A
├── payment-processing/     ← Team C
└── admin-dashboard/        ← Team B
```

When referencing specs in conversation, use `#spec [spec-name]` to load the full context (requirements.md + design.md + tasks.md) for that spec.
