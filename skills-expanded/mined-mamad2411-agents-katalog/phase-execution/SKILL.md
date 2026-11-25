---
name: phase-execution
description: Executes project delivery in five phases (analysis, planning, implementation, validation, delivery) with checklists and a structured final report. Use when the user asks to execute a phase, deliver Phase 1, run a methodological delivery, or follow phased execution.
---

# Phase Execution

Guides execution of a project phase (e.g. Phase 1) in a controlled, traceable way. Execute **only** the requested phase; do not advance to later phases.

## Workflow

Track progress with this checklist:

```
- [ ] Phase 1: Analysis
- [ ] Phase 2: Planning
- [ ] Phase 3: Implementation
- [ ] Phase 4: Validation
- [ ] Phase 5: Delivery
```

### 1. Phase 1 — Analysis (required first)

- **Context**: Analyze scope, objectives, and technical/functional requirements.
- **Dependencies**: Identify links with future phases.
- **Impact**: Assess architectural decisions that affect later tasks.
- **Validation**: Confirm technical and functional understanding before starting.

### 2. Phase 2 — Planning

- **Strategy**: Define the most suitable technical approach.
- **Structure**: Plan code and resource organization.
- **Risks**: Identify possible failures and preventive measures.

### 3. Phase 3 — Implementation

- Implement all components required for the phase.
- Apply project standards (validations, error handling, null safety).
- Optimize PostgreSQL (indexes, constraints, transactions).
- Configure FastAPI, logging, monitoring.
- Include unit tests (minimum 80% coverage).
- Update README, diagrams, and technical docs.

### 4. Phase 4 — Validation

- **Functional tests**: Verify all phase requirements are met.
- **Integration tests**: Validate PostgreSQL and external services.
- **Code review**: Run quality checklist before delivery.

### 5. Phase 5 — Delivery

- Produce a detailed checklist of implemented items.
- Update status in the format below.
- Produce the final report (template below).

## Status update format

Use this template for before/after status:

```markdown
# Before execution
- [ ] Item 1
- [ ] Item 2

# After execution
- [x] Item 1
- [x] Item 2
```

## Constraints

- **Focus**: Execute ONLY the requested phase; do not start the next one.
- **Awareness**: Keep in mind impact on future phases.
- **Quality**: Do not sacrifice quality for speed.
- **Completion**: Finish 100% of the phase before reporting.

## Quality standards (during implementation)

- **Python**: PEP 8, type hints, docstrings.
- **PostgreSQL**: Optimize queries, indexes, constraints.
- **FastAPI**: Pydantic validation, response models, documentation.
- **Architecture**: Separate concerns, dependency injection, logging.

## Final report template

Deliver a report with:

1. **Executive summary**: What was implemented and how.
2. **Completion checklist**: Detailed list of finished items.
3. **Updated files**: Confirmation of status updates.
4. **Technical notes**: Architectural decisions relevant for future phases.
5. **Next steps**: Recommendations for the next phase (do not execute them).
