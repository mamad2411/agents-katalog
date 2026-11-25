---
name: master-engineering-standards
description: Apply the default cross-repo engineering baseline for code quality, maintainability, testing, security, validation, and safe delivery. Use when writing code, reviewing changes, refactoring, planning implementation, or when no more specific skill should dominate.
---

# Master Engineering Standards

This is the default reusable baseline for work across repositories. Apply it unless a more specific skill or project instruction overrides part of it.

## Core defaults

- Improve bad code instead of copying weak patterns.
- Follow existing project conventions when they are sound.
- Prefer root-cause fixes over surface patches.
- Keep changes small, reviewable, and reversible.
- Reuse existing utilities and abstractions before adding new ones.
- Preserve public APIs unless the task requires a behavior change.
- Prefer readability and maintainability over cleverness.

## Quality bar

- Keep functions and modules focused.
- Remove duplication when touching repeated logic.
- Use clear names and consistent structure.
- Add brief comments only where intent is not obvious.
- Avoid speculative abstractions and unnecessary indirection.

## Safety and correctness

- Validate inputs at trust boundaries.
- Handle expected failure paths explicitly.
- Prefer secure defaults and least privilege.
- Never hardcode secrets or commit sensitive values.
- Avoid unsafe string construction for shell, SQL, or HTML contexts.

## Testing and verification

- Add or update tests when behavior changes or regressions are plausible.
- Use types, tests, and linting as executable checks.
- Verify the changed path, not only the happy path.
- If you cannot run validation, say so clearly.

## Delivery habits

- Keep diffs focused on the task.
- Avoid unrelated refactors unless they are necessary to make the change safe.
- Prefer structured logs and actionable error messages for services.
- Include accessibility basics by default for UI work.

## When to reach for more specific skills

- `always-apply-standards` for general coding discipline
- `modern-development-practices` for cross-stack delivery norms
- `testing-patterns` for test strategy and structure
- `security-best-practices` for auth, authorization, and security controls
- `typescript-best-practices` for strict typing and TypeScript patterns
- `error-handling-logging` for error models and structured logging
- `validation-input-sanitization` for schema validation and sanitization
- `api-design-restful` for HTTP API design
- `dry-solid-principles` for refactoring and design quality

## Review checklist

- Is the change solving the right problem?
- Is the touched code better than before?
- Are validation, error handling, and security addressed?
- Are tests or other verification steps adequate?
- Is the result easy for the next engineer to understand?