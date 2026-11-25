---
name: mvp-build-tickets
description: Generate implementation task tickets for a Web MVP. Use after AGENTS.md and agent_docs exist when the user needs small Codex-executable task files with required reading, scope, acceptance criteria, implementation plan, verification checks, risks, and done conditions.
---

# MVP Build Tickets

Create small implementation tickets in `tasks/`.

## Inputs

Read:

- `AGENTS.md`
- `agent_docs/product_requirements.md`
- `agent_docs/tech_stack.md`
- `agent_docs/page_map.md`
- `agent_docs/data_model.md`
- `agent_docs/testing.md`

## Output

Create task files such as:

```text
tasks/
  001-project-foundation.md
  002-core-layout.md
  003-data-model.md
  004-[first-core-feature].md
  005-[second-core-feature].md
  006-polish-and-launch-check.md
```

Each ticket must include:

- Goal
- Required reading
- In scope / out of scope
- Acceptance criteria
- Suggested implementation plan
- Automated and manual verification
- Risks
- Done condition

## Rules

- No ticket should say "build the app".
- Every ticket must be independently verifiable.
- Frontend tickets need browser/manual checks.
- Do not create tickets for Not-in-MVP features.
