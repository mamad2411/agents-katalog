---
name: dotnet-api-review
description: Use this skill when reviewing an ASP.NET Core API for backward compatibility, authentication, persistence and performance risks before it ships.
license: MIT
compatibility:
  - codex
  - claude-code
  - github-copilot
metadata:
  author: skillforge
  version: 1.0.0
allowed-tools:
  - filesystem.read
---

# .NET API Review

Use this skill when reviewing ASP.NET Core APIs. It is also SkillForge's own documentation example, so
it is written the way a real, useful skill should be.

## Goals

- Detect backward compatibility risks before they reach a published contract.
- Review authentication and authorization on every reachable endpoint.
- Identify performance bottlenecks in persistence access.
- Produce findings a developer can act on without further investigation.

## Workflow

1. **Inventory the surface.** List controllers, minimal API endpoints and their routes. Note which are
   anonymous.
2. **Review contracts.** For each request and response type, check whether a change would break an
   existing client: removed fields, narrowed types, changed enum values, altered status codes.
3. **Review authentication.** Confirm every endpoint either requires authorization or is deliberately
   anonymous. Treat a missing attribute as anonymous, not as an oversight to assume away.
4. **Review persistence.** Look for N+1 access patterns, queries without pagination, and unbounded
   result sets.
5. **Report findings ordered by severity**, each with the file, the risk, and the smallest change that
   resolves it.

## What not to do

- Do not rewrite the API's architecture as part of a review.
- Do not report style preferences as risks.
- Do not claim an endpoint is secure. Report what was checked and what was found.

## References

- [API versioning notes](references/api-versioning.md)
