---
name: api-contract-check
description: Protect API request, response, auth, error, and client compatibility.
---

# API Contract Check

## Workflow

1. Identify the route, handler, client, schema, or message contract involved.
2. Read exact request, response, auth, error, and validation definitions.
3. Read affected clients, tests, and API docs.
4. Check backward compatibility and migration implications.
5. Add or update contract tests where behavior changes.
6. Document compatibility notes and verification.

## Boundaries

- Do not change contracts without updating all affected callers and docs.
- Do not expose sensitive errors or provider internals.
- Do not rely on generated maps as contract truth.

## Output

- Relevant files or docs inspected.
- Work completed or plan produced.
- Tests or verification run or recommended.
- Docs updated or skipped with reason.
- Remaining risks, assumptions, and handoffs.
