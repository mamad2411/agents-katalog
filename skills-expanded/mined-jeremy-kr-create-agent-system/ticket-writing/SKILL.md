---
name: ticket-writing
description: "User story-based ticket writing guide. Use when breaking down specs into tickets."
---

# Ticket Writing Guide

## Ticket Format (Medium/Large — EPIC-based)

```markdown
## [EPIC-{number}] {EPIC Title}

### TICKET-{number}: {Ticket Title}
- **User Story**: As a {role}, I want {feature}, so that {value}
- **Acceptance Criteria**:
  - [ ] Criterion 1
  - [ ] Criterion 2
  - [ ] Error handling: ...
  - [ ] Edge case: ...
- **Estimated Effort**: {0.5h ~ 2h}
- **Dependencies**: TICKET-{number} (or "None")
- **EPIC**: EPIC-{number}
```

## EPIC Dependencies
Always include an EPIC dependency map when writing tickets:
```markdown
## EPIC Dependency Map
EPIC-01 (Foundation) → None
EPIC-02 (Preset) → EPIC-01
EPIC-03 (Template) → EPIC-01
```

## Rules
- Max 2 hours for a senior developer, smaller is better
- User story format is mandatory
- Acceptance criteria must include error handling and edge cases
- Dependencies must be explicitly documented
