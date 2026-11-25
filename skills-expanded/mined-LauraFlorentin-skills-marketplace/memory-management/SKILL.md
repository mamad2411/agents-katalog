---
name: memory-management
description: Design short-term and persistent agent memory with consent, provenance, access controls, retrieval, correction, retention, and deletion. Use when a user asks for conversation memory, persistent preferences, cross-session state, long-context summarization, user profiles, or memory retrieval.
---

# Memory Management

Store the minimum durable information that improves the task. Memory is user data, not an unquestioned source of truth.

## Memory classes

- **Working memory:** current-session state and tool results.
- **Episodic memory:** dated prior interactions or events.
- **Semantic memory:** verified durable facts or preferences.
- **Procedural memory:** approved workflows and operating rules.

Keep these classes separate because they have different freshness, privacy, and retention needs.

## Write policy

Before storing, decide whether the item is necessary, authorized, accurate enough, and safe to retain. Record subject, value, source, timestamp, confidence, scope, sensitivity, expiration, and version. Prefer explicit preferences over inferred traits.

Do not store credentials, authentication tokens, sensitive personal data, private reasoning, or third-party data without a lawful, explicit need and suitable controls. Provide correction, export, and deletion paths.

## Retrieval policy

1. Enforce tenant and user access before similarity search.
2. Filter by memory type, scope, time, and sensitivity.
3. Rank by relevance, recency, provenance, and confidence.
4. Inject only the smallest useful set, clearly delimited as untrusted context.
5. Resolve contradictions by asking or preferring a newer explicit user correction.
6. Show when a consequential response relied on stored memory.

Do not use a universal similarity threshold or retention period; calibrate them with task data and risk.

## Lifecycle

Define encryption, audit, retention, expiration, compaction, revalidation, and deletion behavior. Summaries must link back to source events when possible and must not convert uncertain inferences into facts.

Test cross-user isolation, stale and conflicting memories, deletion, correction, prompt injection in stored content, over-retrieval, and behavior when memory is unavailable.
