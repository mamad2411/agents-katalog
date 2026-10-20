---
name: backend-services
description: Structure backend service layers. Use when organizing application
  logic and its boundaries.
metadata:
  tags: backend, services
---

# Backend Services & Application Logic

## Use this skill when
- Organizing use cases and services
- Defining what logic belongs in services vs domain vs controllers
- Wiring repositories, external calls, and transactions

## Do not use this skill when
- Simple CRUD passthrough apps
- Domain modeling decisions (use domain-driven-design)

## Instructions
1. Services implement use cases: orchestrate entities, repositories, and external calls.
2. Keep services in application terms, free of framework/session types.
3. One service per use case boundary; compose rather than grow.
4. Put transactional scope on service operations that mutate.
5. Inject dependencies; avoid hidden globals and service locators.
6. Return results and raise domain errors; map them at boundaries.
7. Keep services testable with in-memory fakes.

## Output Format
- Use case | service | dependencies | transaction scope | errors thrown

## Common Mistakes
- God services with many unrelated methods
- Services reaching into repositories directly for everything
- Framework types (HTTP request objects) inside services
