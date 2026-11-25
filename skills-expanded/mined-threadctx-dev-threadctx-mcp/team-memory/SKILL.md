---
name: team-memory
description: Use the team's shared memory (threadctx) effectively — when to query it, what to write back, and how to write memories a teammate can act on months later. Use whenever starting a non-trivial task, after fixing a non-obvious bug, or after making a decision another developer (or their agent) would need to know.
---

# Team memory (threadctx)

threadctx is the team's shared memory. Anything you store can be recalled later
by you, by a teammate, or by a teammate's coding agent — across Claude Code,
Cursor, and any MCP client. Treat it as writing to a future colleague.

## When to query

Call `memory_query` BEFORE starting work, not after hitting a wall:

- Touching a service, module, or config that looks like it has history
- Fixing a bug that feels like someone may have hit it before
- Making a choice between approaches (a past decision may already settle it)
- Doing anything with deploys, credentials, environments, or CI

Query with a plain-language description of what you're about to do, not
keywords: "adding a new billing webhook handler" beats "webhook".

## When to write

Call `memory_write` AFTER:

- Resolving a non-obvious bug (especially one whose symptom pointed the wrong way)
- Making an architectural or tooling decision, including what was rejected and why
- Discovering a gotcha: a flaky step, a misleading error, an undocumented dependency
- Learning something about the environment that isn't in the repo (account quirks,
  dashboard settings, rate limits)

Don't write things the repo already records (code structure, obvious history) —
write the part that ISN'T visible from the code.

## How to write a memory a teammate can use

A good memory answers three questions without the reader having your context:

1. **What happened / what was decided** — concrete symptom or decision, with
   file paths, commands, error text where relevant.
2. **Why** — the root cause or the reasoning, including dead ends ruled out.
3. **What to do about it** — the action a future reader should take or avoid.

Bad: "Fixed the cache bug in the API."
Good: "GET /api/v1/memory/list served stale data after PATCH because Next.js
Data Cache caches the Neon HTTP driver's fetch() calls even with
dynamic='force-dynamic'. Fix: also set fetchCache='force-no-store' on every
route using an HTTP DB driver. Verify with a mutate-then-read round-trip
against production — the bug only appears on the second read."

## Habits

- One memory per fact. Split unrelated learnings into separate writes.
- Include dates for time-sensitive facts ("as of 2026-07").
- Tag with the subsystem so queries can narrow ("billing", "deploy", "ci").
- If a memory you retrieved turned out to be wrong or stale, write a correction.
