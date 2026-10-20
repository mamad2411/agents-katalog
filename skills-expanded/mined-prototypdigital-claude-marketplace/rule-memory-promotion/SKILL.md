---
name: memory-promotion
description: Session observations never write directly to durable memory — promotion runs through a reviewable consolidation step that dedupes, supersedes, and ratifies.
---

# Memory promotion

The dangerous failure mode is not bad retrieval. It is letting a raw session observation enter durable memory as if it were a ratified constraint. Promotion is the gate that prevents it.

## Rules

- Session observations write to a staging tier, never directly to durable or user-scoped memory.
- Promotion from staging to durable memory goes through consolidation, not a plain append. Consolidation dedupes against existing memories, detects contradictions, and marks superseded entries.
- A promotion that changes user-scoped memory or a stable constraint is reviewable — by the user or a maintainer — before it takes effect. Capability/edge memories may consolidate automatically; judgment/core memories should not.
- Consolidation is the only path that writes durable memory. There is no side door that appends straight to the durable tier.
- Run consolidation on an explicit trigger (idle, session end, or a record-count threshold), not inline on every observation. Inline promotion is how transient staging noise becomes permanent.

"Consolidation is the only path to durable memory" is a non-negotiable invariant: enforce it with a write-path gate (a guarded store API or CI check that rejects direct durable writes), not prose alone — this rule explains why the gate exists.

## Promotion pipeline

```text
observation (in-context)
  -> staging tier            # tagged with provenance
  -> consolidation           # dedup, detect contradiction, mark supersession
  -> [review if core/user]   # a human ratifies stable-constraint changes
  -> durable memory          # only now eligible to guide behavior
```

This mirrors the episodic -> semantic distinction: append-only events stage cheaply; distilled facts are promoted deliberately, deduplicated, and versioned.

## Examples

```text
// BAD — raw session observation written directly to durable memory
session: "user said they prefer tabs"
-> WRITE durable_memory["user.indent"] = "tabs"   // no dedup, no review, no provenance

// GOOD — observation goes through the promotion pipeline
session: "user said they prefer tabs"
-> STAGE { fact: "user.indent=tabs", source: user-stated, session_id: abc123 }
-> CONSOLIDATE (check for contradiction with existing "user.indent=spaces")
-> REVIEW if it's a core preference
-> WRITE durable_memory only after ratification
```
