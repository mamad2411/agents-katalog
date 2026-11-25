---
name: repo-api-contract-design
description: Designs API contracts before implementation across REST, GraphQL, RPC, events, webhooks, SDKs, and service boundaries. Use when adding or changing endpoints, operations, schemas, request/response payloads, pagination, filtering, sorting, validation, or API behavior.
---

# Repository API Contract Design

Use this skill to design or review API contracts before implementation.

## When to Use This Skill

Use this skill when the task involves adding or changing endpoints, operations, events, webhooks, schemas, SDK contracts, request or response payloads, pagination, filtering, sorting, search, validation, OpenAPI, AsyncAPI, GraphQL, protobuf, markdown, or API docs.

## Process

1. Identify the API style and clients.
2. Define the contract before implementation.
3. Define request fields, response fields, errors, auth, pagination, filtering, sorting, and validation.
4. Identify compatibility impact.
5. Identify security and data exposure boundaries.
6. Define examples and documentation updates.
7. Define test evidence before implementation.

## Workflows

Use `workflows/api-contract-design-workflow.md` when designing a new API or changing an existing contract.

## Resources

- `resources/api-contract-checklist.md`
- `resources/api-style-decision-matrix.md`

## Examples

- `examples/api-contract-review-example.md`

## Scripts

This skill owns:

```text
scripts/api-surface-inventory.py
scripts/api-command-guard.py
```

Run scripts with `--help` before manual use.
