---
name: s5-audit-codebase
description: Audit codebase for consistency issues, anti-patterns, and missing test coverage
context: fork
agent: Explore
argument-hint: "[focus-area]"
---

# S5 — Codebase Audit

Audit this codebase for quality issues. Focus area: **$ARGUMENTS**

If no focus area is specified, perform a full audit across all categories.

## Audit Categories

Each category has a detailed checklist in the `checklists/` subdirectory.
Read only the relevant checklist(s) based on the focus area requested.

1. **Naming** — `checklists/naming.md` — snake_case, PascalCase, verb prefixes
2. **Imports** — `checklists/imports.md` — ordering, absolute paths, no wildcards
3. **Error Handling** — `checklists/error-handling.md` — specific exceptions, no bare except
4. **Type Hints** — `checklists/type-hints.md` — annotations, modern union syntax
5. **Docstrings** — `checklists/docstrings.md` — Args/Returns/Raises sections
6. **Test Coverage** — `checklists/test-coverage.md` — happy path, edge cases, fixtures

**If `$ARGUMENTS` specifies a focus area** (e.g., "error handling"), read only that
checklist file. **If no focus area**, read all 6 checklists and audit everything.

## Output Format

For each issue found, report:

```
[CATEGORY] file_path:line_number
  Issue: Description of the problem
  Suggestion: How to fix it
```

End with a summary table:

| Category | Issues Found |
|----------|-------------|
| Naming   | N           |
| Imports  | N           |
| Errors   | N           |
| Types    | N           |
| Docs     | N           |
| Tests    | N           |
