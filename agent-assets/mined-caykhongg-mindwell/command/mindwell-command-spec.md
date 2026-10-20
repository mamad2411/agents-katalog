---
name: spec
description: Spec before code — structured PRD creation for new features
---

# /spec — Specification-Driven Development

> "Plan the work, then work the plan."

## Purpose

Create a comprehensive specification document **before** writing any code. This ensures alignment on requirements, constraints, and acceptance criteria.

## Workflow

### Phase 1: Discovery (Ask Questions)

Before generating a spec, gather requirements by asking:

**Scope**
- What is the objective of this feature?
- Who are the target users?
- What problem does this solve?

**Features**
- What are the core features (MVP)?
- What are the acceptance criteria for each?
- What is explicitly out of scope?

**Technical**
- Any tech stack preferences or constraints?
- Integration points with existing systems?
- Performance requirements?

### Phase 2: Generate Specification

After discovery, produce `SPEC.md` with these sections:

```markdown
# Feature: [Name]

## Objective
[1-2 sentences describing the goal]

## Target Users
[Who will use this and why]

## Core Features
1. [Feature A] — [Acceptance criteria]
2. [Feature B] — [Acceptance criteria]
3. [Feature C] — [Acceptance criteria]

## Out of Scope
- [What we're NOT building in this iteration]

## Technical Approach
- Tech stack decisions
- Data models
- API contracts (if applicable)
- Integration points

## Code Style
- Follow rules in `.claude/rules/`
- [Any feature-specific conventions]

## Testing Strategy
- Unit tests for: [areas]
- Integration tests for: [areas]
- E2E tests for: [critical paths]

## Boundaries
### Always Do
- [Non-negotiables]

### Ask First
- [Decisions requiring approval]

### Never Do
- [Hard constraints]
```

### Phase 3: Review & Confirm

- Present the spec to the user
- Confirm before proceeding to `/plan`
- Save as `SPEC.md` in project root or `docs/specs/[feature].md`

## Output

- `SPEC.md` — The specification document
- Clear alignment on what to build

## Next Step

After spec is approved, run `/plan` to decompose into tasks.
