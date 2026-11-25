---
name: clean-code
description: >-
  Applies minimal-scope, convention-following changes. Use during refactors,
  code review, bug fixes, or when reducing complexity in the repository.
---

# Clean Code

## Principles

1. **Minimize scope** — Smallest correct diff; no drive-by refactors.
2. **Match existing style** — Naming, folder layout, error handling as in neighboring files.
3. **No premature abstraction** — Inline one-off logic; extract only on second real use.
4. **Comments** — Explain business rules and non-obvious logic only.
5. **Tests** — Required for every new feature and bug fix. Unit tests for logic; E2E for critical user flows. Bug fixes need a regression test. See `.agents/skills/developer-quality/SKILL.md`.
6. **Readable names** — Do not use single-character variable names. Use descriptive names so intent is clear without reading surrounding code.
7. **Early return** — Prefer guard clauses and early returns over nested `if/else` chains.
8. **Fail fast** — Prefer assertions and throwing errors over returning `{ success: boolean }` or silent failure flags.

```typescript
// Prefer
function parseAmount(raw: string): number {
  if (!raw.trim()) {
    throw new Error("Amount is required");
  }
  const parsed = Number(raw);
  if (Number.isNaN(parsed)) {
    throw new Error("Amount must be a number");
  }
  return parsed;
}

// Avoid
function parseAmount(raw: string): { success: boolean; value?: number } {
  if (!raw.trim()) {
    return { success: false };
  }
  // ...
}
```

## Monorepo

- Shared types: prefer duplication over wrong coupling until a shared package exists.
- Use workspace scripts from the repo root as documented in `project-context` / root README.

## TypeScript

- Follow `.agents/skills/typescript/SKILL.md` for strict mode, ESLint, explicit types, and module conventions.
- Strict types at boundaries (DTOs, API client).
- Avoid `any`; use discriminated unions for variant data.

## Security

- No secrets in repo; validate all inputs server-side.
- Protected routes and mutations require auth.

## Review self-check

- [ ] Change solves the stated problem only
- [ ] No single-character variable names; names describe intent
- [ ] Early returns used instead of deep if/else nesting where applicable
- [ ] Errors thrown (or framework HTTP exceptions) instead of boolean success flags
- [ ] Lint passes on touched packages
- [ ] Automated tests pass; new/changed behavior has test coverage
- [ ] User-facing strings unchanged unless the task requested copy changes
- [ ] Docs updated if behavior or env vars changed
