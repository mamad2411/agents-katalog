---
name: modern-development-practices
description: Apply current cross-stack development norms—AI-assisted workflows, supply-chain hygiene, observability, API contracts, accessibility, and safe refactors. Use when planning features, reviewing code, upgrading stacks, or when the user asks about modern engineering practice beyond a single language.
---

# Modern Development Practices

General engineering habits that complement language-specific skills. Prefer concrete project conventions when they conflict.

## AI-assisted coding

- Treat generated code like a junior PR: run it, read the diff, and verify edge cases; do not merge blind refactors.
- Keep changes small and reversible; one concern per commit or PR when possible.
- Use tests, types, and linters as executable specs—add or extend them when behavior changes.
- Never commit secrets, tokens, or production connection strings; scan diffs for accidental `.env` or key material.

## Dependencies and supply chain

- Commit lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, etc.) for applications; pin versions for reproducible builds.
- Prefer fewer, well-maintained dependencies over micro-packages; audit critical paths (auth, crypto, parsing).
- Automate dependency updates with CI and a defined review bar; do not ignore high-severity advisories on exposed surfaces.

## Observability and operations

- Prefer structured logs (JSON or key-value fields) over unstructured strings; include request or correlation IDs across service boundaries.
- Define what “healthy” means (readiness vs liveness); expose metrics or traces where the stack supports them.
- Fail loudly in development, fail safely in production—user-facing errors should be actionable, not stack dumps.

## APIs and contracts

- Treat the API as a product: version intentionally, document breaking changes, and use deprecation periods when clients exist.
- Machine-readable contracts (OpenAPI, JSON Schema, protobuf) should stay in sync with implementation; generate clients or types where practical.
- Idempotency and clear error models matter for retries and mobile or flaky networks.

## Frontend and product quality

- Build accessibility in by default: semantic HTML, labels, focus order, and keyboard paths—not only visual polish.
- Prefer composition (small components, hooks, composables) over large “god” modules that mix data, UI, and side effects.

## Data and migrations

- Schema changes should be backward compatible when systems roll out gradually; pair migrations with application logic that tolerates old and new shapes during cutover.
- Back up or snapshot before destructive migrations in shared environments.

## Security posture (see also security-best-practices)

- Assume least privilege for services and humans; rotate credentials that appear in chat or logs.
- Validate and normalize input at trust boundaries; encode output in the right context (HTML, SQL, shell).

## When to reach for other skills

- **TypeScript / Vue / Node** → language and framework skills in this library.
- **REST design** → api-design-restful.
- **Errors and logging** → error-handling-logging.
- **Tests** → testing-patterns.

**Principle:** Ship small, observable, reviewable changes; let tools and contracts carry intent so the next human—or agent—can continue safely.
