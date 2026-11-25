---
name: memory-layer-bridge
description: Teaches agents when to query Cipher/Mem0, when to consult Obsidian, and when to log decisions inline — routing context retrieval to the right memory layer.
category: mcp
tags: [memory, obsidian, cipher, mem0, context-management, rag]
agents: [opencode, freebuff, antigravity, codex]
---

# memory-layer-bridge

This skill is the standing memory routing contract for all agent sessions. It is **always-on** — it defines which memory layer to query and when, preventing wasted LLM context and ensuring decisions are persisted to the right store.

## Purpose

Route agent memory operations to the correct layer: short-term inline context, Mem0/Cipher semantic memory, or Obsidian vault structured notes. Prevent agents from hallucinating past decisions, duplicating retrieval work, or logging to the wrong store.

## Invocation

**OpenCode / Codex:** `Invoke memory-layer-bridge`
**Freebuff:** `/skill memory-layer-bridge`

## Memory Layer Decision Tree

```
What are you trying to do?
│
├─ Recall a past decision, preference, or fact about the user/project
│       → Query Mem0 / Cipher first (semantic search)
│       → Fall back to Obsidian vault search if not in Mem0
│
├─ Look up a structured document (architecture, plan, meeting note, log)
│       → Query Obsidian vault directly (note title or tag search)
│
├─ Access session-scoped context (current task, open files, recent output)
│       → Use inline context window; do not hit external memory stores
│
├─ Log a significant decision, change, or discovery
│       → Write to Obsidian vault (permanent, searchable, linked)
│       → Also update Mem0 if it is a preference or fact about the user
│
└─ Log a homelab event or infrastructure change
        → obsidian-homelab-logbook (structured Obsidian note)
        → homelab-logbook (audit trail entry)
```

## Rules

1. **Query before generating.** Before producing a plan or architecture, check Mem0/Cipher for past decisions on the same topic.
2. **Write durable facts to Obsidian.** Any decision worth keeping longer than the session belongs in the vault.
3. **Never duplicate across layers.** If something is in Obsidian, do not re-log it to Mem0 unless it is a distilled preference/fact.
4. **Inline context is ephemeral.** Do not rely on conversation history for facts that span sessions.
5. **Log code architecture decisions.** Any ADR (Architecture Decision Record) goes to `Projects/<project>/decisions/` in the vault.

## Inputs

- Memory operation intent: recall, log, search, or update
- Topic or entity being queried/logged
- Optional: session type (coding, homelab, music, planning) for routing context

## Outputs

- Retrieved facts, decisions, or structured documents from the appropriate layer
- Confirmation that a log/write was routed to the correct store
- Routing explanation when the decision is non-obvious

## Failure Modes

- Mem0/Cipher unreachable — fall back to Obsidian vault search; log retrieval failure inline.
- Obsidian vault unreachable — queue writes; surface to user for manual paste.
- Conflicting records across layers — surface both to user; do not silently choose one.

## References

- [Mem0 documentation](https://docs.mem0.ai/)
- [Obsidian Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api)
- [Retrieval-Augmented Generation overview](https://arxiv.org/abs/2005.11401)

## Companion Skills

- `obsidian-vault-manager` — vault write/read operations
- `git-safe-ops` — log significant code decisions (parallel always-on)
- `homelab-safe-ops` — log infrastructure decisions (parallel always-on)
- `homelab-logbook` — structured homelab event logging
- `obsidian-homelab-logbook` — vault-native homelab log layer
