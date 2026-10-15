---
name: golang-ddd-cqrs
description: "Structure Go application logic with pragmatic CQRS. Use when command and query concerns are mixed, handlers are hard to test, one application service is becoming wide, or a Go service needs business-oriented command and query naming, separate handlers, thin ports, narrow consumer-owned interfaces, and guidance on when CQRS is or is not worth the cost."
user-invocable: true
license: MIT
compatibility: Designed for Codex, Claude Code, Gemini CLI, Cursor, OpenCode, and similar AI coding agents working with Go services.
metadata:
  author: joeyave
  version: "0.3.0"
---

# Golang DDD CQRS

Use this skill to split application logic into clear commands and queries without turning Go code into ceremony-heavy enterprise scaffolding.

## Start Here

- Use CQRS when a service has meaningful write-side behavior, mixed read and write models, or application services that are hard to reason about.
- Skip or minimize CQRS when the service is mostly simple CRUD or login-like flows with little business behavior.

## Workflow

1. Split the use cases into writes and reads.
- Commands mutate state and may return errors.
- Queries return data and should not perform business mutations.

2. Name them in business language.
- Prefer `ScheduleTraining`, `CancelTraining`, `ApproveReschedule`, `AvailableHours`.
- Avoid default CRUD names unless the business really speaks that way.

3. Introduce separate handlers when it improves clarity.
- Use one command handler type per command when the logic or dependencies differ.
- Use one query handler type per query when read concerns differ.
- Keep interfaces narrow and owned by the handler that consumes them.

4. Keep handlers orchestration-only.
- Domain rules belong in the domain layer.
- Transport mapping belongs in ports.
- Database or external API details belong in adapters.

5. Shape the ports around CQRS.
- HTTP or gRPC ports may call commands directly.
- If a create command needs a follow-up read, prefer `204 No Content` plus `content-location` when practical, or execute an explicit query after the command.
- Keep port-specific error translation at the edge.

6. Test the application layer as orchestration.
- Mock repositories and outbound services with tiny handwritten mocks.
- Keep business-scenario assertions in domain tests unless the behavior truly belongs to application orchestration.

## Guardrails

- Do not create separate command and query packages if the service is still trivial.
- Do not let commands return large read models by default.
- Do not hide business logic in command handlers just because they are convenient.
- Do not keep one giant application service if separate handlers would shrink interfaces and tests.

## Use These References

- Read [references/cqrs-guidelines.md](references/cqrs-guidelines.md) for naming, packaging, and tradeoffs.
- Read [references/application-tests-and-errors.md](references/application-tests-and-errors.md) for handler testing and transport-agnostic errors.

## Deliverables

- command and query boundaries that match the use cases,
- business-oriented names,
- narrow handler-owned interfaces,
- thin transport code,
- handler tests focused on orchestration instead of domain internals.
