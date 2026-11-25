---
name: nestjs-best-practices
description: NestJS best practices — 40 rules across modules, DI, error handling, security, performance, testing, database, API design, microservices, and deployment. Use when writing, reviewing, or refactoring NestJS code.
---

# NestJS Best Practices

Comprehensive best practices guide for NestJS applications. Contains 40 rules across 10 categories, prioritized by impact to guide automated refactoring and code generation.

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Architecture | CRITICAL | `arch-` |
| 2 | Dependency Injection | CRITICAL | `di-` |
| 3 | Error Handling | HIGH | `error-` |
| 4 | Security | HIGH | `security-` |
| 5 | Performance | HIGH | `perf-` |
| 6 | Testing | MEDIUM-HIGH | `test-` |
| 7 | Database & ORM | MEDIUM-HIGH | `db-` |
| 8 | API Design | MEDIUM | `api-` |
| 9 | Microservices | MEDIUM | `micro-` |
| 10 | DevOps & Deployment | LOW-MEDIUM | `devops-` |

## How to find a rule

Each rule lives in its own file under [`rules/`](rules/), named `<prefix>-<rule>.md` (e.g.
`rules/arch-avoid-circular-deps.md`, `rules/security-validate-all-input.md`); the prefixes map
to the category table above and [`rules/_sections.md`](rules/_sections.md) lists every rule per
category. Read only the rules the task touches — each file carries the why, an incorrect and a
correct code example, and extra context.
