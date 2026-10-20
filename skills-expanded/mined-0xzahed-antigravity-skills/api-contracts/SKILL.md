---
name: api-contracts
description: Design clear, consistent API contracts. Use when defining
  endpoints, schemas, and semantics.
metadata:
  tags: api, contracts
---

# API Contract Design

## Use this skill when
- Designing REST/GraphQL/RPC endpoints
- Defining schema, naming, and status semantics
- Reviewing contracts for consistency and evolvability

## Do not use this skill when
- Implementing endpoints in a framework (use framework skills)
- Documenting (use openapi-engineering)

## Instructions
1. Define the resource model and operations first, then choose verbs/status.
2. Name resources as nouns and keep URLs hierarchy logical and short.
3. Never expose internal field names; use API vocabulary.
4. Define consistent field naming: casing policy, dates as ISO-8601, enums as strings.
5. Specify status codes precisely: 200/201/204, 4xx for client errors with validation details.
6. Handling pagination, filtering, and sorting consistently.
7. Design for evolution: additive changes, versioning strategy, tolerance to unknown fields.
8. Write the contract in OpenAPI and keep implementation in sync.

## Output Format
- Resource map | endpoint spec | field conventions | versioning policy

## Common Mistakes
- URLs exposing DB concepts
- Inconsistent error shapes across endpoints
- Breaking contracts without a migration plan
