# LangChain Memory & Workflows

## Summary

**One-sentence:** Picks the right LangChain memory backend (buffer/summary/vector/entity) and emits a decision-record + wired RunnableWithMessageHistory config for the chosen shape.

**One-paragraph:** Conversational LangChain apps live or die by their memory shape. Buffer memory is the safe default under 10 turns; beyond that you need summary, vector, or entity memory — each with its own tradeoffs (lossy compression, semantic drift, brittle extraction). This methodology converts a conversation profile (expected turn count, recall pattern, security posture, store backend) into a deterministic memory choice, emits the `RunnableWithMessageHistory` wiring, and records the decision so the next reviewer can audit it.

**Ефективно для:** solopreneur dev shipping a multi-turn assistant who needs the cheapest memory shape that still answers "as I mentioned earlier" prompts correctly.

## Applies If (ALL must hold)

- Building a conversational LangChain (or LangGraph) app where users reference earlier turns.
- Conversation has any persistence requirement (same session across requests, or multi-session recall).
- Token budget per turn is bounded (you cannot just dump the full history every time).
- You control the chain wiring (can swap `get_session_history` and the message history class).
- Production target runs ≥1 process — i.e. an in-process dict will not survive restart.

## Skip If (ANY kills it)

- Single-turn, stateless Q&A — memory adds latency and zero value.
- Throwaway notebook prototype with no users — pick `InMemoryChatMessageHistory` and move on.
- Conversation has hard regulatory ban on history persistence (some healthcare/finance flows).
- You are on serverless without any external store (Redis/Postgres) and cannot add one.
- Target framework is LlamaIndex or vanilla Anthropic SDK — different memory primitives, use a different methodology.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `conversation-profile.yaml` | YAML with `expected_turns`, `recall_pattern`, `entity_focus`, `ttl_seconds`, `store_backend` | author writes by hand, ≤20 lines |
| Existing chain | Python `Runnable` instance | the chain you want to wrap with memory |
| Store backend credentials | env vars (`REDIS_URL`, `DATABASE_URL`, …) | infra config, never inlined |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[langchain-basics]] | foundational LangChain runnable + LCEL knowledge |
| [[max-turns-circuit-breaker]] | memory bloat is the most common cause of runaway turn budgets |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 18 testable rules for memory selection + LangGraph state | ~1200 |
| `content/02-output-contract.xml` | essential | Decision-record JSON schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Session ID leakage, summary loss, vector cross-session, in-memory store death | ~700 |
| `content/04-procedure.xml` | recommended | 6-step selection + wiring procedure | ~900 |
| `content/06-decision-tree.xml` | essential | Memory-type selection tree by turns × recall pattern | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Profile parsing + rule firing | haiku | Deterministic dispatch, no creativity needed. |
| Decision-record drafting | sonnet | Explains tradeoffs in prose; needs sound reasoning. |
| Wiring code emission | sonnet | Mechanical but must compile against the user's chain. |
| Cross-check vs rules + failure modes | opus | Catches subtle session-isolation and TTL gaps. |

## Templates

| File | Purpose |
|---|---|
| `templates/conversation-profile.yaml` | Input contract — 8 fields the methodology consumes. |
| `templates/decision-record.md.j2` | Output skeleton: chosen memory type + rejected alternatives + wiring snippet. |
| `templates/decision-record.md` | Output skeleton: chosen memory type + rejected alternatives + wiring snippet. Generated from `templates/decision-record.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/wiring-snippet.py` | Working `RunnableWithMessageHistory` wiring for Redis-backed buffer memory. |
| `templates/_smoke-test.yaml` | Minimum viable profile that drives the methodology end-to-end. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-langchain-memory.py` | Validates a decision-record against the JSON schema in `02-output-contract.xml`. | Before committing the output; pre-commit hook. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[langchain-workflows]] — LangGraph state machines; memory feeds workflow state.
- [[llamaindex-chat-engine]] — same problem, different framework — cross-reference when comparing.
- [[max-turns-circuit-breaker]] — pair to cap turn count alongside memory choice.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree branches on `expected_turns`, then on `recall_pattern` (recency vs semantic), then on `entity_focus`. Each leaf maps to a rule id in `01-core-rules.xml` so the agent always cites which rule drove the choice — and can be replayed for audit.
