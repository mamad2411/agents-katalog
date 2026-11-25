# Customer Block Project Guidelines

## Code Style

### Typescript / Bun

- Prefer `for..of` instead of `forEach`
- Use `import type { ... }` instead of `import { ... }` if the imports are only types
- Do not use template literals if interpolation and special-character handling are not needed.
- Be strict when it comes to typing (no `any`, no `unknown`)

### SQL

- Keywords in UPPERCASE (SELECT, FROM, WHERE)
- Column/table identifiers in snake_case, quoted when necessary
- Indent CTEs and subqueries consistently (4 spaces)
- Use aliases for table names
- Break long lines at logical points (after commas, operators)
- Use CTEs for complex queries instead of nested subqueries
- Use QUALIFY for row filtering where appropriate
