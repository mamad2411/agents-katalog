---
name: syncolab-cognitive-memory
description: Guides Syncolab Cognitive Memory Layer (CML)—Qdrant + Mem0 composite, tenant scope, REST memory endpoints, and TS agent recall/persist. Use for long-term memory hydration and external runtime memory_layer contracts.
---

# Syncolab Cognitive Memory (CML)

## Purpose

Apply platform long-term memory rules: composite Qdrant + Mem0 storage, strict tenant scope (account + user + agent), TS agent recall/persist hooks, and external runtime `memory_layer` hydration—without inventing tenant IDs or storing secrets in memory text.

## When to Use

- Agent recall or persist of long-term memory in Managents TS phase graph.
- External runtime memory via hydrated `memory_layer` (POST query/write under `restPathPrefix`).
- Questions about CML architecture, Mem0 behavior, or tenant-scoped IDs.

## When NOT to Use

- Project documentation search → **syncolab-living-docs** (SKS).
- Generic vector RAG over arbitrary indexes → **vectorize**.
- Storing secrets, tokens, or credentials in memory payloads.

## Expected Outcome

- Memory operations respect account/user/agent scope.
- External calls use Bearer JWT from hydration; never spoof `accountId`/`userId`.
- Writes go to the composite stack (Qdrant vectors + Mem0 when enabled)—not assumed single store.

## Inputs to Gather

- Whether the runtime is TS agent (recall_memory / extract_and_persist_memory) or external hydration.
- Stable external IDs: `acct-{accountId}:user-{userId}`, `acct-{accountId}:agent-{agentId}` for Mem0 when applicable.
- `memory_layer.enabled`, endpoints, and `stackMode` from hydration only when present.

## Workflow

1. Confirm memory backends and hydration are enabled before query/write.
2. **TS agents**: use **recall_memory** at intake when enabled; persistence pipeline after run for extract/persist.
3. **External runtimes**: use `memory_layer.endpoints` relative paths—**POST …/query** and **POST …/write** with session auth.
4. Never put secrets into memory text; never invent tenant identifiers.
5. For product semantics, align with Mem0 docs when behavior is unclear.

### TS agent (phase graph)

- **recall_memory** at intake when enabled.
- **extract_and_persist_memory** / persistence pipeline after the run.
- Stores: **Qdrant** (vectors) and **Mem0** (signal layer) when enabled—composite, not one physical store.

### Tenant scope

- Scope is always **account + user + agent**.
- External IDs: `acct-{accountId}:user-{userId}`, `acct-{accountId}:agent-{agentId}` for Mem0.

### External runtimes (Syngle, OpenClaw, Copilot)

- Hydration includes **`memory_layer`**: `endpoints`, **`auth`** (Bearer JWT), **`stackMode`**, **`agentPromptHint`**, **`enabled`** only with backends + hydration `userId`.
- Use **POST …/query** and **POST …/write**; server derives auth identity—do not spoof ids.

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| memory_layer + REST | Query/write per hydration contract. |
| TS graph hooks only | Recall/persist via platform pipeline. |
| Disabled backends | Report; do not fake memory hits. |

### Related tool sets

- (none declared)

## Review / Decision / Execution Criteria

- Minimal PII in stored memories.
- Distinguish recall (read) vs persist (write) paths.

## Output Format

1. Operation (query/write/recall/persist).
2. Scope used (account/user/agent).
3. Result summary without leaking raw sensitive memories.
4. Pointer to architecture doc when explaining design.

## Quality Bar

- Accurate composite-store semantics.
- No fabricated memory entries.

## Safety and Boundaries

- No secrets in memory text.
- No cross-tenant access or spoofed IDs.
- Confirm before bulk delete if supported.

## Escalation / Dispatch Rules

- Canonical docs → **syncolab-living-docs**.
- Vector search over non-CML indexes → **vectorize**.

## References

- Architecture: `readme/syncolab/cml-memory-layer.md` (platform repo).
- Mem0: https://docs.mem0.ai/
- Legacy: `skills/old_skills.json` (`syncolab-cognitive-memory`).
- `skills/skill.instruction.md`, `skills/meta.instructions.md`
