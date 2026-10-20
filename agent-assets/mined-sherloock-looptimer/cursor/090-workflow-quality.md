---
description: Workflow and quality guardrails: linting, docs hygiene, and dev server management.
alwaysApply: false
---

## Code style and structure
- Write concise, technical TypeScript.
- Prefer iteration and modularization over code duplication.
- Use descriptive variable names with auxiliary verbs (e.g., `isLoading`, `hasSolution`).
- Keep functions small and focused (single responsibility).
- Add comments only for complex logic (explain **why**, not what).

## Development server management
- Do not automatically start or restart the dev server (`npm run dev`).
- Only suggest running the server when explicitly needed for testing.

## Linting and code quality
- Never introduce unused variables/imports; remove immediately.
- In catch blocks, omit unused error param: `catch { ... }`.
- Prefix intentionally unused variables with underscore: `_unused`.
- After substantive edits, run lint checks and fix new issues.

## Documentation hygiene
- Don’t create new documentation files for every small change.
- Update existing docs/README only when behavior/setup changed.

## Workflow
- If the user explicitly requested a change, proceed without asking for confirmation.
- When relevant, include the exact app version from `package.json` in the answer.
