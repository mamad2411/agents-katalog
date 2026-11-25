---
name: implementation-clean-code
description: Implement the approved design in clean, maintainable code, keep changes aligned with requirements, and leave the codebase ready for review with unit tests and lint-clean output where practical.
---

# Implementation Clean Code

Use this skill when acting as the developer in this repository.

## Goals
- Implement the design faithfully.
- Produce maintainable code that follows the clean-code standard.
- Leave the change ready for technical review.

## Required Inputs
- `doc_templates/requirements/current.yaml`
- `doc_templates/design/current.yaml`
- `.ai-team/framework/clean-code.md`
- Relevant code in `src/`

## Required Outputs
- Updated implementation in `src/`
- Unit tests for relevant new or changed behavior

## Procedure
1. Implement only the approved scope.
2. Follow the clean-code standard during the change, not as a cleanup step afterward.
3. Add or update unit tests for all relevant new or changed logic.
4. Run linting when available and fix warnings or violations where practical.
5. Escalate back to architect or coordinator when the code change would alter structure, major patterns, library choices, or significant runtime behavior.

## Quality Bar
- Clear naming
- Small focused units
- Separation of concerns
- Explicit error handling
- No avoidable lint errors
- No missing unit tests for relevant behavior
