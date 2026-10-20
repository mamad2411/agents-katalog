---
name: document-code-contracts
description: Document function, method, and package callable contracts directly from a codebase. Use when Codex needs to formalize what a callable expects, returns, throws, mutates, or guarantees, and when the result should be stored in a repository under docs/contracts/. Name each contract file with the camelCase function or method name being documented.
---

# Document Code Contracts

## Goal

Write implementation-backed contract docs for callables. Store each contract in `docs/contracts/<camelCaseCallable>.md`.

## Workflow

1. Identify the real callable seam.
   - Start from the user-named function, method, export, or package surface.
   - Read the implementation, declared signature or types, relevant tests, and a few meaningful call sites.
   - If the user asks for a whole package, start with public exports or other caller-facing entry points.

2. Extract only contract-relevant facts.
   - Signature and overloads
   - Inputs: required fields, optional fields, defaults, accepted unions, normalization
   - Returns: sync or async shape, nullable cases, sentinels
   - Errors: thrown errors, error results, validation failures
   - Preconditions: auth, setup, feature flags, required state
   - Side effects: database writes, network calls, events, cache invalidation, mutations
   - Guarantees: ordering, idempotency, transaction boundaries, persistence, compatibility promises

3. Create or update the contract file.
   - Ensure `docs/contracts/` exists.
   - Default path: `docs/contracts/<camelCaseCallable>.md`.
   - For methods, use the method name as the filename base.
   - Convert `snake_case`, `kebab-case`, spaced names, and `PascalCase` to `camelCase`.
   - If the base filename collides with a different callable, append the narrowest useful owner suffix only when needed, for example `createUserAdminService.md`.
   - Use `scripts/init_contract_doc.py <symbol>` to scaffold when useful.

4. Write the contract.
   - Follow `references/contract-template.md`.
   - Keep every statement grounded in code, tests, or explicit runtime behavior.
   - Prefer repository-relative source paths.
   - Mark uncertainty explicitly instead of inventing guarantees.
   - If behavior is messy, document current behavior first. Separate desired behavior only when the user asked for design work.

5. Keep scope sharp.
   - Write one file per callable by default.
   - For package requests, create multiple small contract files instead of one giant overview unless the user explicitly wants a package summary.
   - Update an existing contract file instead of creating a near-duplicate.

## Quality Bar

- Match callable names and type spellings from code.
- Prefer the real runtime seam over wrappers, generated types, or stale comments.
- Capture caller-relevant behavior, not internal trivia.
- Do not copy large source blocks into the contract.
- Label anything inferred from usage or tests as an inference.

## Output Shape

Include these sections unless the repo already has a stronger contract format:

- `Summary`
- `Symbol`
- `Signature`
- `Location`
- `Inputs`
- `Returns`
- `Errors`
- `Preconditions`
- `Side Effects`
- `Guarantees`
- `Examples` when an example meaningfully clarifies behavior
- `Source of Truth`

## Resources

- `scripts/init_contract_doc.py`: Scaffold `docs/contracts/<camelCaseCallable>.md`.
- `references/contract-template.md`: Default structure and naming examples.
