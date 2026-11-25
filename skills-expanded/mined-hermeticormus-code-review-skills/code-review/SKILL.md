---
name: code-review
description: Domain-aware code review for an everyday diff or pull request. Classify the code's domain (algorithm, API, security, data, UI, infrastructure), then review for the failure modes that domain actually has. Use when reviewing a change. For production-readiness use mars-skills; for security hardening use vibe-proof-skills.
license: MIT
---

# Code review

Review the everyday diff or pull request by classifying the code's domain first, then applying the checklist for that domain. One generic pass over all code surfaces formatting nits and misses the failure mode that ships the incident.

## 1. Review the change, not the file

Read the diff, not the whole file. Read enough surrounding context to judge correctness, no more. A finding outside the diff matters only if the change made it newly reachable or newly wrong.

## 2. Classify the code domain

| Domain | Indicators | Review focus |
|---|---|---|
| Algorithm | Loops, recursion, data structures, sorting or searching | Complexity, edge cases, correctness |
| API or network | HTTP, requests, endpoints, REST, GraphQL | Error handling, rate limiting, auth, validation |
| Security | Auth, crypto, passwords, tokens, user input | OWASP top 10, injection, data exposure |
| Data | SQL, ORM, database, queries, transactions | N+1, indexes, consistency, migrations |
| UI or frontend | React, components, DOM, CSS, events | Accessibility, performance, state |
| Infrastructure | Docker, K8s, CI/CD, configs, scripts | Security, idempotency, failure modes |

A change can span domains. Apply each matching checklist; do not pick one silently.

## 3. Apply the matching focus checklist

- Algorithm: correctness for all inputs, Big-O, edge cases (empty, single, max, duplicates), readability of the invariant.
- API or network: error handling on timeout and 4xx/5xx, input validation before business logic, auth and authz, rate limiting and idempotent retries.
- Security: input validation at the boundary, injection (SQL, command, XSS, template, deserialization), secret handling, server-side access control.
- Data: N+1 queries, transaction atomicity and isolation, index usage at production row counts, backward-compatible migrations.
- UI: accessibility, render performance, state correctness, effect cleanup and async races.
- Infrastructure: least privilege, idempotent apply, partial-failure and rollback path, observability.

## 4. Assign severity to every finding

- Critical (must fix): wrong output, data loss, security hole, broken contract. Blocks merge.
- Improvement (should fix): correct but fragile, slow at scale, missing a newly reachable edge case.
- Nitpick (optional): naming, style, clarity.

A finding you cannot assign a severity to is not yet specific enough to report.

## 5. Structure the feedback

```text
## Summary
[1-2 sentence overview of what the change does]

## Domain: [detected domain(s)]

## Critical (must fix)
- [ ] [file:line] Description + concrete suggestion

## Improvements (should fix)
- [ ] [file:line] Description + concrete suggestion

## Nitpicks (optional)
- [ ] [file:line] Description

## What's correct
- Observation the author got right
```

Every finding cites a location and proposes a direction, not just a complaint.

---

See full content at https://github.com/HermeticOrmus/code-review-skills.
