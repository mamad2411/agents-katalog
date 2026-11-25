---
name: agent-memory-design
description: Design persistent memory for LLM agents and assistants so they remember facts across turns and sessions without bloating the context window. Use when building chatbots, coding agents, or copilots that must recall user preferences, prior decisions, and project facts beyond what fits in-context.
source: self
date_added: 2026-05-01
---

# Agent Memory Design

The context window is RAM. Memory is disk. This skill covers how to externalize what the model needs to "remember" so it can be retrieved on demand instead of held resident — preserving recall without paying tokens for it on every turn.

Pairs with `../engineer/engineer-toolkit/context-window-management/` (in-window tactics) and `./llm-engineering/` (broader RAG/agent system design).

## When to Use

- Agent forgets user preferences, prior decisions, or earlier corrections after the window rolls over.
- Long-running coding/research sessions degrade as history grows.
- You're tempted to "just use a bigger model" to fix forgetting.
- Multiple agents/sessions need to share state about the same user, repo, or task.
- You need auditability: who/what wrote a memory, when, and why.

## Mental Model: Memory Tiers

| Tier | Lifetime | Storage | Read pattern | Example |
| --- | --- | --- | --- | --- |
| Working | Single call | In-context | Always present | Current task prompt, scratchpad |
| Session | Single conversation | Rolling summary + recent turns | Auto-injected | "User is debugging auth flow in repo X" |
| Long-term semantic | Persistent | Vector store / KV | Tool-call recall | "User prefers tabs, not spaces" |
| Long-term episodic | Persistent | Append-only log + index | Tool-call recall | "On 2026-04-12 we decided to drop Redis" |
| Procedural | Persistent | Files / skills | Auto-loaded by topic | Coding conventions, runbooks |

Rule: if a token doesn't change the *next* answer, it shouldn't be in the window — push it down a tier.

## Storage Backends

Pick the simplest that meets recall and latency needs. Combine when needed.

- **Markdown / JSON files** — best for procedural memory and small fact stores. Diffable, reviewable, version-controllable. Used by Claude/Copilot "memory" features and Cursor rules.
- **SQLite + FTS5** — structured facts, scoped queries, transactional writes. Great default for single-user agents.
- **Vector store** (pgvector, Qdrant, LanceDB, Chroma) — semantic recall over unstructured episodic memory. Required when keys aren't known in advance.
- **KV store** (Redis, DynamoDB) — session summaries, per-user preferences, rate-limited writes.
- **Graph store** (Neo4j, Kuzu) — entity/relationship memory (people, repos, decisions and their links). Optional; usually overkill before scale.

Hybrid pattern: vector store for recall, SQLite/KV for canonical facts, files for human-editable procedural memory.

## Write Policies

What goes in memory matters more than how it's stored.

- **Explicit signals first.** "Remember that…", thumbs-up/down, accepted suggestions, committed code.
- **Implicit extraction second.** Summarize each turn into candidate facts; require a confidence threshold before persisting.
- **Dedupe on write.** Embedding similarity > 0.9 → merge or skip. Otherwise the store fills with paraphrases.
- **Contradiction handling.** New fact conflicts with old → keep both with timestamps and prefer newest on read; or run a reconciler. Never silently overwrite.
- **Decay / TTL.** Episodic memories age out; semantic preferences don't. Tag every memory with `created_at`, `last_used_at`, and a category-based TTL.
- **Provenance.** Store source (user message id, file path, tool output) so the agent can cite and the human can audit.
- **PII boundary.** Classify on write. Block secrets and regulated data unless the user opted in. See `../security/data-classification/`.

## Read Policies

- **Tool-call recall, not auto-injection** for long-term memory. Give the agent a `recall(query, k, filters)` tool and let it decide. Auto-injection wastes tokens and biases reasoning.
- **Auto-inject only the rolling session summary + top-N pinned facts** (e.g., user identity, current repo, active task).
- **Top-k with a quality floor.** Drop hits below a similarity threshold rather than always returning k.
- **Recency + relevance scoring.** `score = α·similarity + β·recency + γ·usage_count`. Tune per tier.
- **Budget per call.** Cap memory tokens to a fixed % of the window (e.g., 10–15%). Truncate by score.

## Compaction Loops

Inspired by MemGPT/Letta and modern coding-agent harnesses:

1. Append every turn to an episodic log.
2. When session tokens exceed a threshold, summarize the oldest N turns into one or more semantic facts.
3. Move summarized turns out of the live window; keep them retrievable via recall.
4. Periodically re-summarize summaries (hierarchical compaction) to bound storage.

Keep the most recent 2–5 turns verbatim — summaries lose the detail the model needs for immediate follow-ups.

## Reference Architecture

```
┌─────────────┐     ┌──────────────────┐
│   Agent     │◄───►│  Memory Manager  │
└─────┬───────┘     └─┬────────┬───────┘
      │               │        │
      │       recall()│        │write()
      │               ▼        ▼
      │        ┌──────────┐ ┌──────────┐
      │        │  Vector  │ │  SQLite/ │
      │        │  Store   │ │  KV/Files│
      │        └──────────┘ └──────────┘
      │
      ▼
  Context window:
   - system prompt
   - pinned facts (≤ N)
   - rolling session summary
   - recent turns (verbatim)
   - tool results (current task)
```

The Memory Manager is the only component that touches storage. The agent interacts via tools: `recall`, `remember`, `forget`, `list_memories`.

## Evaluation

You can't tune what you don't measure.

- **Recall@k on past facts.** Seed known facts, ask questions later, measure retrieval hit rate.
- **Forgetting rate.** % of previously-stated facts the agent contradicts after N turns.
- **Memory precision.** % of recalled memories that are actually relevant to the query.
- **Token cost per task.** Compare with/without memory tier; memory should reduce average tokens, not just shift them.
- **Latency budget.** Recall p95 < 200 ms or it'll dominate user-perceived latency.
- **Hallucination delta.** Does memory reduce or increase fabrication? Bad recall is worse than no recall.

## Anti-Patterns

- **Stuffing all history into the prompt.** Linear cost, "lost in the middle," and rate-limit pain. Use compaction.
- **Auto-injecting top-k vector hits every turn.** Biases the model toward stale or irrelevant facts.
- **One giant `memory.md` file.** Becomes unsearchable. Split by scope (user / project / session) and topic.
- **Silent overwrites.** Destroys auditability and breaks contradiction handling.
- **Storing raw chat logs as "memory."** That's a transcript, not memory. Memory is extracted facts with provenance.
- **No forgetting.** Memory grows unbounded, recall precision falls, costs rise.
- **Sharing memory across users without isolation.** Privacy incident waiting to happen.

## Minimal Viable Memory (Start Here)

For a single-user coding agent:

1. One markdown file per scope: `memory/user.md`, `memory/repo.md`, `memory/session/<id>.md`.
2. Auto-inject `user.md` + `repo.md` (cap ~500 tokens total).
3. On each turn, append a one-line note to the session file if anything decision-worthy happened.
4. At session end, ask the model to extract durable facts and propose edits to `user.md` / `repo.md`. Human approves diffs.
5. Add a vector store only when file-grep recall stops being good enough.

Ship this, measure forgetting rate, then evolve.

## Related

- `../engineer/engineer-toolkit/context-window-management/` — in-window selection, compression, summarization
- `./llm-engineering/` — RAG, agent harness, evals, guardrails
- `../engineer/ai-api-development/` — provider integration patterns
- `../security/data-classification/` — what may be persisted, and where
