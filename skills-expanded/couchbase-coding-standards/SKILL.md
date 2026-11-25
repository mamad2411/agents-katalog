---
name: couchbase-coding-standards
description: "Apply coding standards and a style guide for writing production application code against Couchbase, combining general software-engineering best practices (naming, functions, error handling, testing, docstrings, version control, code review, secrets hygiene) with Couchbase-specific conventions (SDK idioms, document-key naming, exception and retry handling, durability, parameterized SQL++, connection lifecycle). Use whenever the user asks about coding standards, code style, a style guide, clean code, naming conventions, structuring Couchbase application code, idiomatic SDK usage, how to write or review Couchbase code, code-review checklists, linting, formatting, testing Couchbase code, or best practices for writing Couchbase apps. Distinct from couchbase-app-integration (SDK mechanics: pooling, durability, scan consistency) and couchbase-data-modeling (document design) — this is the how-to-write-and-review-the-code layer on top of them. Use proactively when reviewing or authoring code that touches Couchbase."
license: MIT
---

# Couchbase coding standards & style guide

A skill for *writing and reviewing* clean, correct, maintainable application code against Couchbase. It combines general software-engineering discipline with the Couchbase-specific conventions that keep application code idiomatic, safe, and resilient.

Distinct from:
- `couchbase-app-integration` — SDK *mechanics* (connection pooling, durability levels, scan consistency, retry primitives). This skill assumes those mechanics and covers how to *write the code* around them well.
- `couchbase-data-modeling` — *what shape* the documents take. This skill covers *how the code that reads and writes them* is structured and named.
- `couchbase-sqlpp-tuning` — query *performance*. This skill covers query *safety in code* (parameterization, injection, result handling).

If the conversation is "how should this Couchbase code be written / named / structured / reviewed," this is the right skill.

## When this skill applies

- "What are the coding standards / style guide for Couchbase apps?"
- "Review this Couchbase code."
- "How should I name my document keys / SDK objects / functions?"
- "Is this idiomatic use of the SDK?"
- "How do I handle Couchbase errors properly in code?"
- "How do I write testable code against Couchbase?"
- "How do I avoid SQL++ injection?"
- "Set up linting / formatting / a review checklist for a Couchbase project."

## Pick the right reference

| Question | Read |
|---|---|
| "General clean-code standards — naming, functions, comments, tests, version control, reviews, secrets" | `references/general-coding-standards.md` |
| "Idiomatic SDK use — connection lifecycle, KV vs query, batching, async, per-language idioms" | `references/couchbase-sdk-idioms.md` |
| "Document key + field naming conventions, type discriminators, metadata fields" | `references/key-and-document-conventions.md` |
| "Couchbase exceptions, retry/backoff, idempotency, durability in code, transactions hygiene" | `references/error-handling-and-resilience.md` |
| "Writing SQL++ in application code safely — parameterization, injection, scan consistency, pagination" | `references/sqlpp-in-code.md` |

## Core principles

**Principle 1 — Idiomatic beats clever.**
Each SDK has a grain: Python uses context managers and type hints, Java uses reactive streams / `CompletableFuture`, Node uses promises/async-await, Go uses explicit error returns. Code that fights the SDK's idioms is harder to read, review, and maintain. Follow the grain of the language and the SDK, not a house dialect imposed across all of them.

**Principle 2 — Correctness at the boundary is a coding standard, not an afterthought.**
Couchbase code fails in specific, recurring ways: transient errors, timeouts, ambiguous durability, missing documents, CAS mismatches, injection through string-built SQL++. Handling these is not "extra hardening" bolted on later — it is part of writing the code correctly the first time. Every read can miss; every write can be ambiguous; every query built from user input is an injection risk until parameterized.

**Principle 3 — Optimize for the reader and the reviewer.**
Code is read far more than written. Names carry intent, functions do one thing, keys are self-describing, and the non-obvious "why" is commented (never the obvious "what"). A reviewer should be able to tell *what* a document key refers to, *whether* an error path is handled, and *why* a durability level was chosen — from the code alone.

**Principle 4 — Verify version-sensitive symbols; never assert an SDK API from memory.**
SDK method names, option objects, and exception types differ across major SDK versions and drift over time. Pin every version-sensitive symbol against the project's actual SDK version (check existing usage in the codebase first, then the versioned SDK docs). If a symbol can't be verified against the pinned version, flag the line rather than guessing. This applies to review feedback as much as to authored code.

## Using this skill to review code

When reviewing, walk these in order and cite the specific reference for any issue found:

1. **Correctness** — reads that can miss, writes with unhandled ambiguity, unparameterized SQL++, CAS/idempotency gaps → `error-handling-and-resilience.md`, `sqlpp-in-code.md`
2. **Idiom** — fighting the SDK grain, connections opened per-operation, blocking calls in async paths → `couchbase-sdk-idioms.md`
3. **Naming & shape** — opaque keys, missing type discriminators, inconsistent field naming → `key-and-document-conventions.md`
4. **General hygiene** — function size, naming, comments, tests, secrets in code → `general-coding-standards.md`

Report findings direct over diplomatic: state the issue, cite the standard, show the fix. Flag opinions as opinions, separate from correctness defects.

## Related skills

- `couchbase-app-integration` — the SDK mechanics this skill's idioms sit on top of
- `couchbase-data-modeling` — document design that the key/field conventions here serialize
- `couchbase-sqlpp-tuning` — query performance (this skill covers query *safety in code*)
- `couchbase-transactions` — transaction semantics referenced by the resilience guidance here
- `couchbase-security-hardening` — cluster-side security; this skill covers app-side secrets/injection hygiene
