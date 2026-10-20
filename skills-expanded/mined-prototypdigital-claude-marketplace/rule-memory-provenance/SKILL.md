---
name: memory-provenance
description: Every durable memory carries provenance — source, time, confidence, and whether it was user-stated or agent-inferred. No silent writes.
---

# Memory provenance

A memory without provenance is an unattributable claim. When recall surfaces it later, you cannot tell whether it is a ratified user constraint or a guess the agent made three sessions ago. Attribution is what makes a memory store auditable instead of append-only.

## Rules

- Every durable memory record carries, at minimum: source, observed-at timestamp, confidence, and origin (user-stated vs agent-inferred).
- Never write a memory silently. A write is an event with an author — record who proposed it and on what evidence.
- Keep user-stated and agent-inferred memories distinguishable at the storage layer, not only by convention. They carry different authority — see memory-recall-authority.
- When a memory changes, append the new value with its own provenance instead of overwriting in place. The prior value and its source remain part of the audit trail.
- If a fact cannot be attributed to a source, it does not get promoted to durable memory. Unattributed inference stays in-context and expires with the session.

## Minimal record shape

```text
fact:         "deploys go through a PR, never direct to main"
source:       user-stated            # user-stated | agent-inferred | imported
observed_at:  2026-06-13T15:00:00Z
confidence:   high                    # high | medium | low
supersedes:   <record-id | null>
```

The exact schema is yours to choose; the four provenance fields are not optional. Because this is a hard schema invariant, enforce it with a write-time validation gate (schema check or CI) that rejects records missing any of the four fields — do not rely on this prose alone.

## Examples

```text
// BAD — memory record with no attribution
{ fact: "user prefers dark mode" }

// GOOD — memory record with full provenance
{
  fact:        "user prefers dark mode",
  source:      "user-stated",
  observed_at: "2026-06-15T10:00:00Z",
  confidence:  "high",
  supersedes:  null
}
```
