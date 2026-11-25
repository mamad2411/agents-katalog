---
name: create-manual-test-cases
description: Create or update manual QA test case documents from requirements, tickets, descriptions, source code, or documentation using a named template or previous test case sample. Use for functional, regression, sanity, UAT, black-box, white-box, or non-functional manual test cases.
---

# Create Manual Test Cases

## Required References

Before writing or updating manual test cases, read the exact source materials relevant to the request:

1. The requirement, ticket, feature description, API spec, design doc, existing test plan, source code, or documentation named by the user.
2. The manual test case template named by the user.
3. At least one previous or sample manual test case named by the user, when available.

If the user does not name a template, look for a project-standard manual test case template in likely QA, testing, docs, or development-plan locations. If no template or sample exists, ask the user for one before writing final manual test cases. A draft may be produced only when clearly labeled with the assumed structure.

Use previous test cases as style and detail references. Do not treat a previous test case as the canonical template unless the user says to.

## Modes

Support one or more user-requested test design modes:

- `functional`: Cover expected feature behavior, user flows, business rules, and acceptance criteria.
- `regression`: Cover existing behavior that must continue working after a change.
- `sanity`: Cover the smallest high-confidence set of major paths after a build, deploy, or change.
- `UAT`: Write business-readable cases for end users, stakeholders, or acceptance review.
- `black-box`: Derive cases from visible behavior, requirements, UI, API contracts, and docs without relying on implementation details.
- `white-box`: Use implementation details, source paths, branches, validation logic, persistence, integrations, and error handling.
- `non-functional`: Cover quality attributes such as accessibility, performance, compatibility, reliability, security, usability, or recoverability.

If the user does not specify a mode, default to `functional` and include relevant `regression` cases when the source material describes existing behavior or a changed feature.

## Workflow

1. Confirm the requested scope, mode, source materials, template, and sample references from the prompt.
2. Read the source materials and exact template or sample files before writing.
3. Extract testable requirements, user flows, data rules, permissions, edge cases, negative paths, integrations, and acceptance criteria.
4. Map each test case to a source requirement, section, ticket, or assumption whenever possible.
5. Write test cases using the template structure exactly, preserving field names and formatting.
6. Include clear titles, preconditions, test data, steps, expected results, priority, type or mode, and traceability fields when the template supports them.
7. Mark unclear behavior as an assumption or open question instead of inventing product behavior.
8. Review for duplicate, vague, untestable, or overly broad cases before finishing.

## Boundaries

- Do not execute tests or claim pass/fail results unless the user explicitly provides execution results or asks to perform execution.
- Do not invent requirements not supported by source materials.
- Do not expose secrets, credentials, tokens, or private data in test data.
- Do not replace automated test coverage when the user specifically asks for executable tests.
- Do not change the project template unless the user asks to update it.

## Output

- Source materials, template, and sample test cases inspected.
- Test modes used.
- Manual test cases created or updated.
- Assumptions, open questions, and coverage gaps.
- Any files changed, or the recommended target file if no file was written.
