---
name: legacy-code-comprehension
description: Read and understand an unfamiliar/legacy codebase safely before changing it — entry points, dependency tracing, behavior mapping, characterization tests, seams. Use during onboarding of an existing project or before any change in code you did not write.
category: meta-process
---

# Legacy Code Comprehension

Discipline for understanding code you did not write, BEFORE touching it. Guessing on a running system
is how regressions are born (R-024: claims cite sources; brownfield ask-don't-infer).

## Reading order (outside-in)

```text
1. RUN IT first if possible: build + start + existing tests. What you observe beats what you assume.
2. Entry points: main/server bootstrap, route tables, cron/queue consumers, CLI commands.
3. Money paths: follow the 2-3 most important user flows end-to-end (request -> handler -> data).
4. Data model: schema/migrations tell you the domain truth faster than the code does.
5. Boundaries: external calls (HTTP clients, queues, SDKs), config/env reads, feature flags.
6. Conventions: naming, error handling, DI style — record them; your changes must match (R-006-19).
```

## Map what you learn (evidence, not vibes)

```text
- Every statement about the system carries file:line or command output (R-024-04).
- Record into knowledge: component profile, context_hints, conventions.md, test-policy.
- Unknowns are listed as unknowns with a question — never silently assumed.
```

## Before changing anything

```text
- CHARACTERIZATION TESTS: if the area you must change has no tests, first write tests that pin the
  CURRENT behavior (even if "wrong") — then change with the safety net.
- SEAMS: prefer introducing a seam (interface/adapter/wrapper) over editing tangled internals.
- BLAST RADIUS: list callers/consumers of what you change (grep imports/routes/events) into
  impact_analysis before the first edit.
- Smallest change that satisfies the task — no drive-by refactors (task fidelity).
```

## Smells that demand a user question (do not guess)

```text
Dead-looking code that is actually reachable; duplicated logic with subtle differences; config that
contradicts docs; tests that are skipped/commented; TODOs around the change area; behavior that
differs between environments.
```
