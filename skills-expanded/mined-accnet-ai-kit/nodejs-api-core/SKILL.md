---
name: nodejs-api-core
description: Implementation pattern for a Node/TypeScript API layer — repository (data access) → service (business logic/selection) → creation/transaction flow, using authenticated identity for ownership/authorization decisions. Use when building or changing API service/repository code. Test code stays in the project.
version: 0.2.0
tier: stack
stack: [node, typescript, api]
owner: backend
gates: [G2, G3]
related: [.ai/modules/backend.md, api-contract, test-and-validation]
---

# Skill: nodejs-api-core

## Purpose
A reusable, project-agnostic pattern for the API core so selection/creation logic is consistent and testable, independent of any host skill.

## When to use
Building or changing an API's repository, service, or creation/transaction layer in Node/TypeScript.

## Pattern
```
repository (data access)  ->  service (business logic / selection)  ->  creation / transaction flow
```
- **Repository**: pure data access. All filtering/constraints belong here (scope, status, capacity, owning identity). Mock the DB client (e.g. `pool.query`) in tests.
- **Service**: decision logic over repository results. Cover the primary choice, each fallback branch, and a clear "no candidate available" error. Mock the repository in tests.
- **Creation / transaction flow**: wraps the write in a transaction and passes the authenticated identity down — never trusts a client-supplied id for ownership or placement.

## Rules
- **Use the authenticated identity for authorization/placement** — from the auth context, not the request body.
- Enforce constraints (scope, status, capacity) in the query, not only in app logic.
- Every decision branch has a matching test (`test-and-validation`).
- Signature/DTO changes go through `api-contract`; schema/data changes go through `data-migration`.

## Checklist
- [ ] Filtering/constraints in the repository query
- [ ] Service covers primary + each fallback + no-candidate error
- [ ] Authenticated identity threaded through the flow
- [ ] Each branch tested; boundary asserted
- [ ] Contract/schema changes routed to the right skill

## Anti-patterns
- Business/selection logic leaking into the repository or the controller
- Trusting a client-supplied owner/user id for placement
- Only the happy path implemented/tested

## Output
Repository/service/flow code in the project + task status in `tasks.md`. Migrations follow `data-migration`.
