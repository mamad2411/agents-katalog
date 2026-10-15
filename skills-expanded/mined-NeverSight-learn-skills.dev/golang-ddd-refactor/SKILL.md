---
name: golang-ddd-refactor
description: "Refactor existing Go code toward a behavior-first, invariant-protecting domain model. Use when business rules live in handlers or repositories, shared structs couple DB and API models, entities expose setters or mutable public fields, or a service needs domain methods, constructors, private state, repository update closures, and focused domain tests."
user-invocable: true
license: MIT
compatibility: Designed for Codex, Claude Code, Gemini CLI, Cursor, OpenCode, and similar AI coding agents working with Go services.
metadata:
  author: joeyave
  version: "0.3.0"
---

# Golang DDD Refactor

Use this skill when the code already works but is becoming hard to trust, test, or extend because the business rules are scattered across transport and persistence code.

## Refactor Loop

1. Find the use case from the edge of the system.
- Start from HTTP handlers, gRPC methods, commands, repository callbacks, or transaction blocks.
- Write down the business operation in plain language before introducing any new types.

2. Extract the rules hiding inside conditionals.
- Look for "walls of `if`" that decide whether something may happen.
- Turn those rules into invariants and behavior methods on a domain type.

3. Create or tighten the domain type.
- Prefer constructors that reject invalid state.
- Prefer private fields when external mutation would bypass invariants.
- Replace setters with behavior methods named in business language.

4. Make the domain database-agnostic.
- Remove Firestore, SQL, protobuf, or HTTP concerns from domain packages.
- Introduce separate persistence models if storage shape differs from the domain shape.

5. Rebuild the repository boundary.
- Put the repository interface next to the code that consumes it.
- Prefer generic repository capabilities such as load or update over repository methods that mirror every business action.
- Use closure-based update methods when the write requires transactional read-modify-save behavior.

6. Add black-box tests around the domain.
- Test exported behavior, not private fields.
- Use helpers that create meaningful domain objects such as "available hour" or "canceled training".
- Keep mocks out of domain tests.

7. Shrink the old code paths.
- Make handlers, services, and repositories delegate to the new domain behavior.
- Delete duplicated validation once the domain enforces it reliably.

## Guardrails

- Do not invent entities and value objects unless they clarify real business behavior.
- Do not move pure transport validation into the domain unless it is a business rule.
- Do not leak database transaction types or clients into the domain.
- Do not keep public writable fields just because the old code used them.

## Use These References

- Read [references/domain-rules.md](references/domain-rules.md) for the core rules adapted for this skill pack.
- Read [references/refactor-playbook.md](references/refactor-playbook.md) for a step-by-step migration path and anti-pattern checklist.

## Deliverables

- behavior-oriented domain methods,
- constructors or factories that enforce validity,
- narrowed repository contracts,
- removed duplicated business checks from handlers or adapters,
- focused domain tests that describe the behavior in business terms.
