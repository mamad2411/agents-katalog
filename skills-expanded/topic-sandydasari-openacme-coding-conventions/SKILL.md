---
name: coding-conventions
description: Workforce coding conventions — read existing patterns, prefer narrow types, leave the surface area smaller than you found it.
tags: [engineering, coding, style]
---

# Coding conventions

Generic guardrails for any agent that writes or modifies code. Load this skill when you're about to touch a codebase you don't fully own.

## Read before you write

Read the file you're about to modify. Read its callers. Read the test that covers it. The shape that already exists is the shape — match it. Don't introduce a new file layout, a new abstraction, or a new dependency just because it feels cleaner to you in isolation.

## Smallest viable change

The diff should answer the request and nothing else. If the request says "fix bug X," your diff fixes bug X — it does not also reformat the file, rename three identifiers, extract a helper, or upgrade a dependency. Each of those is a separate decision the user has not made yet.

Three similar lines beats a premature abstraction. Wait for the fourth before factoring.

## Comments

Default: don't write one. Names and types do the explaining. Add a comment only when the *why* is genuinely non-obvious — a hidden invariant, a subtle ordering constraint, a workaround for a specific upstream bug. Keep it one line. Don't explain *what* the code does; the reader can see that.

Never write multi-paragraph docstrings. Never reference the current ticket or the caller list — both rot.

## Types

Prefer narrow types over `any` / `unknown` / wide unions. Make illegal states unrepresentable when it's cheap.

When validating data crossing a boundary (HTTP, files, env vars), validate once at the boundary and trust the type inside. Don't re-validate in every internal function.

## Errors

Throw `Error` with a clear, specific message. Don't swallow. Don't wrap in `try/catch` just to log-and-rethrow.

Don't add error handling for cases that can't happen. Trust internal invariants; only validate at boundaries.

## Dependencies

Don't add a dependency for something you can write in 20 lines. Don't add a dependency that pulls in 200 transitive packages for one helper.

When you do add one, prefer the standard already in use in this repo over a "better" alternative. Consistency beats individual optimization.

## Ask before guessing

When the requirement is ambiguous, ask. Don't infer the user's intent from one example and ship the inferred behavior. A two-sentence question saves a re-do.

## Tests

A bug fix gets a test that would have caught the bug. A new feature gets at least one happy-path test. If a function has no tests today and you're adding new behavior, add the test for the new behavior — don't backfill the existing surface.

Tests live next to their code (the `test/` dir in this package, or alongside the file in others — match the local convention).
