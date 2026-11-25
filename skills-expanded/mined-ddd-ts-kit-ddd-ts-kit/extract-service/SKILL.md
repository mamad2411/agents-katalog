---
name: extract-service
description: >-
  Use when the user mentions microservices, splitting the monolith, deploying or scaling one
  context alone, when a context needs data or a synchronous answer from another, or on
  context/extractable.
argument-hint: "<context>"
allowed-tools:
  - Bash(npx ddd-ts-kit check *)
  - Bash(npx ddd-ts-kit list *)
  - Bash(npx ddd-ts-kit generate *)
  - Bash(npm test *)
---

# Extractable contexts

Context: `$ARGUMENTS`

A modular monolith is the default deployment; a context that must leave does so by changing
composition and adapters only. If extraction would require editing `domain/` or
`application/`, the boundary was already broken.

## The rules that keep it true

| Rule | Check |
|---|---|
| The context owns its data: its own database schema, no foreign key, join or query on another context's tables | `context/extractable`, `context/published-language-only` |
| No transaction spans two contexts. One decides, the other reacts | handlers save one aggregate of one context |
| Collaboration by integration events, published through the outbox, consumed idempotently | `events/outbox-required`, `events/consumer-idempotent` |
| A synchronous need (a price, a credit check) goes through a port of the caller, bound as `gateway`. In process today, HTTP or RPC tomorrow: same port, timeouts and failure handled from day one | `layer/application-inward` |
| Data needed often from another context is a local projection fed by its events, not a call | review |
| The context assembles with the kernel and the platform only (its declarations or its module) | per-context boot test |
| Configuration is read through the platform and namespaced by context | review |
| No shared mutable state, no singleton shared across contexts | `context/extractable`, `composition/only-in-module` |
| Authorization travels as an actor in the message, never as a session | `authz/actor-explicit` |

`npx ddd-ts-kit check --rule context/extractable` and the generated
`test/architecture/extractable.spec.ts` wire each context alone, with the kernel and the
platform only: a hidden dependency on another context makes it fail.

## When one context needs another

1. Does it need to *react* to something that happened there? Integration event.
2. Does it need *data* to decide, repeatedly? Local projection updated by events; accept
   that it is eventually consistent, and say so in `CONTEXT.md`.
3. Does it need an *answer now* and cannot decide without it? A port and a gateway adapter
   (`npx ddd-ts-kit generate gateway <ctx> <upstream> <Name>`), with a timeout and a stated
   behaviour when the other side is down.
4. Does it need to *change* the other's state in the same transaction? Then either the two
   are one context, or the requirement must become a process: one step, an event, the next
   step, with compensation. Go back to `ddd-ts-kit:bounded-contexts`.

## Extracting

1. `npx ddd-ts-kit generate service <context>`: `src/apps/<context>/main.ts` composing that
   context, the kernel and the platform, with its own start script and compose service
   (the same image, another entry point), and `deployable` in the config. The context
   **leaves the whole application**: `src/main.ts` and the worker compose `hostedContexts`
   (every context but the extracted ones, listed in the `extracted` regions of the composition
   root), so its consumers, processes, jobs and routes run in the service only, and
   `everyContext` stays the full list for the contracts and the end-to-end tests. Its
   scheduled jobs leave with it, the jobs of the platform (`audit.verify`, `audit.archive`,
   `privacy.purge-expired`, `events.purge-published`, `jobs.purge-finished`) stay with the whole application (the service composes with
   `platformJobs: false`), and every container shares one `DEPLOYMENT_NAME` while its
   `OTEL_SERVICE_NAME` stays its own. `test/architecture/hosting.spec.ts` composes both roots and
   proves nothing is registered twice (`npx ddd-ts-kit generate worker` gives the jobs of the
   remaining contexts a process of their own).
2. Replace each in-process `gateway` adapter that points to it, in the remaining contexts,
   by a remote adapter of the same port. Same contract suite.
3. Switch the event provider from in-memory to a broker for both sides (`stack.broker`:
   outbox relay on the producer, one durable subscription per consumer name). Nothing changes
   in handlers.
4. Move the context's schema and migrations with it; the others never read it, so nothing
   else moves.
5. The published language becomes a versioned package or stays a shared source folder: it
   is a contract either way.
6. Document in `docs/context-map.md` (skill `ddd-ts-kit:context-map`) and a decision record: what is deployed where, and the new failure
   modes (the other side can now be down).

Do not extract for its own sake: a separate deployment buys independent scaling and release
at the price of distributed failure. The point of these rules is that the option stays cheap.
