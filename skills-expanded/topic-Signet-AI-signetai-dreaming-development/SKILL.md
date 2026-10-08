---
name: dreaming-development
description: "Use for Signet Dreaming development: inspect existing source, semantic-memory, retrieval, and inference architecture before changing it; prevent duplicate modules and ad-hoc providers."
---

# Dreaming Development

Use this skill to preserve Signet's current architecture while changing
Dreaming. Treat this as a development guide, not the Dreaming runtime prompt
or a feature plan.

## Start from the codebase

Fetch the current base branch before reading architecture. Establish the
existing design from fresh `origin/main`, then compare the task branch. Read
the relevant implementation, its callers, tests, and retrieval consumers before
proposing a design. Locate the current owners for:

- source capture, artifact persistence, and purge;
- source selection and aggregation;
- transcript, summary, and compaction lineage;
- semantic memory and graph writes;
- retrieval and ranking;
- inference routing and Pi integration.

Do not infer an owner from old docs, an issue, a previous implementation, this
skill, or a stale checkout. The freshly fetched base branch is authoritative.

Load only the skills needed for the task. Do not load an old Dreaming workflow
or a broad unrelated toolkit merely because the task mentions Dreaming.

## Keep the layers distinct

```text
episodic evidence → source selection → Dreaming → semantic memory
                                                  ↓
                                        semantic-first retrieval
```

**Episodic evidence** is immutable, provenance-bearing source material:
artifacts, transcripts, compactions, summaries, imports, and native-harness
memory. Preserve its content, time, identity, source structure, and scope.
Do not make ingestion decide what becomes a memory. Do not rewrite evidence
when a conclusion changes.

**Semantic memory** is derived, current understanding: memories, entities,
claims, and relationships. Dreaming can create, reinforce, supersede, merge,
or leave it alone. Every conclusion must point back to evidence. Preserve
attribution; “X believes Y” is not automatically “Y is true.”

**Retrieval** searches both layers. Prefer semantic results for normal recall;
retain episodic results for proof, temporal drill-down, deep history, and
questions without a semantic conclusion.

Source-native topology is episodic structure, not semantic knowledge. Do not
pollute semantic entities with source folders, documents, headings, or links.

## Respect handoffs

1. Capture source material into the existing episodic substrate.
2. Reuse the existing shared source selector, or merge duplicated selectors
   into its real owner. Never add another aggregator beside one already there.
3. Give Dreaming bounded episodic evidence plus relevant semantic context.
4. Keep validation, scope, provenance, deduplication, idempotency, and writes
   in the daemon's existing shared write path.
5. Let the daemon or an external agent perform reasoning, but keep them on the
   same source-selection and apply contracts. External agents do not write the
   database directly.

Keep compactions and temporal lineage available as episodic/retrieval input.
Do not delete a summary or lineage path until its non-Dreaming responsibilities
have been traced and rehomed.

## Reuse infrastructure

Before adding a module, queue, reader, provider, or API, search for the current
equivalent and extend or consolidate it. A new abstraction must remove real
duplication immediately; it cannot be a parallel implementation.

For inference, use the existing daemon inference router and workload resolver.
Pi-backed model routes and the existing ACPX harness route are both behind that
contract. Do not add a direct vendor client, invented endpoint, model default,
or second provider layer unless the current code has no applicable contract and
that absence has been demonstrated.

Trace the active route before changing inference: workload resolver → daemon
router → provider factory → Pi or ACPX backend. Bind Dreaming to that route;
never call Pi or a vendor SDK directly from a Dreaming worker.

Scope all reads and writes with the data model's agent, visibility, project,
session, and harness boundaries. Preserve source removal and forgetting:
purging evidence removes its derived retrieval views without rewriting
unrelated semantic knowledge.

## Finish cleanly

Prove the replacement against capture, compaction, semantic writes, and
retrieval. Then make one cutover: migrate callers and delete the duplicate
reader, runner, or writer. Do not ship compatibility readers, fallback runtime
paths, or a second source of truth.
