---
name: memory-recall-authority
description: Rank recalled memory by authority, not only relevance — and never let stale, contradicted, or superseded memory present as a current constraint.
---

# Memory recall authority

Relevance tells you a memory is on-topic. Authority tells you whether it is allowed to guide behavior. Assembling context that conflates the two — where an unratified or superseded memory sits beside a current constraint as if equal — is a context-assembly failure, not a retrieval failure.

## Rules

- Label every recalled memory by authority level, not only by relevance or similarity score. A higher similarity score never outranks a lower authority level.
- Stale, contradicted, or superseded memories are retained as audit history but excluded from default recall. They answer "what did we once believe," not "what should I do now."
- Treat a recalled memory as background context to verify against current state, not as a binding instruction. Before acting on a memory that names a file, flag, or decision, confirm it still holds.
- When two recalled memories conflict, resolve by authority then recency before use. Never carry both into reasoning silently.
- Never let agent-inferred or session-staged memory override a user-stated constraint.

## Authority ordering (default)

```text
1. Ratified user constraint   (user-stated, reviewed)     -> guides behavior
2. Durable agent-inferred     (consolidated, attributed)  -> guides; verify if load-bearing
3. Staged observation         (this session, unpromoted)  -> context only, never binding
4. Superseded / contradicted  (audit history)             -> excluded from default recall
```

This is the recall-side companion to memory-promotion: promotion decides what enters durable memory, authority decides what durable memory is allowed to drive.

## Examples

```text
// BAD — acting on a superseded memory because similarity score is high
recalled: { fact: "deploy target is staging", authority: superseded, score: 0.97 }
-> used as binding instruction  // wrong: superseded memory should not guide behavior

// GOOD — filter by authority before acting
recalled: { fact: "deploy target is staging", authority: superseded, score: 0.97 }
-> excluded from active context; surfaced only if user asks "what did we once believe?"

recalled: { fact: "deploy target is production", authority: ratified-user-constraint, score: 0.85 }
-> used to guide behavior despite lower score
```
