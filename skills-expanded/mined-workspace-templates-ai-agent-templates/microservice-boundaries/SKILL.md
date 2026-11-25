---
name: microservice-boundaries
description: Finds real seams in a monolith, assigns data ownership, and proposes a migration order that extracts one service at a time with a clear reason.
---

# Microservice boundaries

Find seams in the evidence. Do not draw them on a whiteboard.

## Steps

1. Map the modules: directories or packages, and for each one the tables it reads and writes (grep for table names, ORM models and raw SQL), the modules it imports, and who commits to it (`git shortlog -sn -- <path>`).
2. Build the dependency picture: count imports between modules in both directions and count cross-module joins and shared tables. Two modules that write the same table are one service until proven otherwise.
3. Score candidates. A good seam has few inbound calls, a table set nobody else writes, a distinct rate of change or scaling need, and one owning team. Rank candidates by this score.
4. For the top candidate, list every call that would become a network call, with its frequency and whether it is in a user-facing request path. More than a few synchronous calls per request means the seam is wrong.
5. Define data ownership: the service owns its tables; others read through an API or a replicated read model fed by events. Name the events.
6. Plan the extraction: first isolate behind an interface inside the monolith, then move the tables to a separate schema, then run the new service in parallel, then switch the traffic, then delete the old code.
7. Estimate cost honestly: deployment, monitoring, tracing, local development and distributed failure handling.

## Rules

- Never propose shared databases between services as the end state.
- Never propose more than one extraction at a time.
- If no seam scores well, recommend a modular monolith and list the boundaries to enforce with lint rules.

## Report

The map, ranked candidates with evidence, the recommended first extraction with its steps, and the risks.
