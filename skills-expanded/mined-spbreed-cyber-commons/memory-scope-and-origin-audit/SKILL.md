---
name: memory-scope-and-origin-audit
description: >-
  Audit what an agent's persisted memory is keyed by and whether the origin of
  each record survives the write, then show what a poisoned record does to a
  later request from a different user. Use when reviewing memory, RAG stores or
  any state that outlives one session.
allowed-tools: Read, Grep, Glob
---

# A memory write is a durable authorisation decision

Poisoning a session lasts a session. Poisoning memory lasts until somebody
notices, and the damage lands on **a different user's** request — which is why
the key and the origin field matter more than the content filter.

## When to use this

Reviewing any store the agent writes to and later reads back: conversation
memory, a vector index it maintains, a summaries table, a "learned preferences"
record.

## Procedure

**1 — Read the write path, not the read path.** Find every call that persists.
Record the key it writes under and every field it stores.

**2 — Answer the two questions about the key.** Is it scoped to the *writer* —
the user whose content produced it — or to something wider, a workspace, a
tenant, the agent itself? A key wider than the writer is the mechanism by which
one user's content reaches another's session.

**3 — Check whether origin survives the write.** A record derived from an
untrusted document is itself untrusted. If the write drops the origin, the
poison is indistinguishable from a fact on read, and no later control can
recover the distinction.

**4 — Age the payload.** Write from one user's untrusted content, then read
back from a different identity and a later request. The gap is the point: a
memory finding that only reproduces inside one session is a session finding.

**5 — Check expiry and revocation.** Ask what removes a record, and who can
trigger it. "Nothing" is a common and reportable answer.

## Example

**Input** — the fixture committed at the top of [`scripts/memory_scope_and_origin_audit.py`](scripts/memory_scope_and_origin_audit.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — from a real run, the two write sites and what removal reaches:

```
  "writes": [
    {"site": "cybertravels/memory.py:remember()",
     "key_scope": "workspace", "origin_stored": true},
    {"site": "cybertravels/knowledge/retriever.py:_summarise_and_cache()",
     "key_scope": "workspace", "origin_stored": false}
  ],
  "cross_user_reachable": true,
  "aged_probe": {"written_by": "dana@...", "read_by": "priya@...",
                 "steered": true},
  "expiry": {"mechanism": "manual",
    "revocable_by": "memory.forget(owner) covers only remember() records;
      _summarise_and_cache() entries have no TTL and no delete path, so the
      laundered summary (seq 3) cannot be revoked by anyone"}
```

Dana wrote it, Priya read it four days later, and neither is an attacker. The
second write site is the finding: same store, same key, and the origin column
gone — so on read the vendor's sentence is indistinguishable from policy.

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "writes": [{"site": "str", "key_scope": "writer|workspace|tenant|agent", "origin_stored": false}],
  "cross_user_reachable": true,
  "aged_probe": {"written_by": "str", "read_by": "str", "steered": true},
  "expiry": {"mechanism": "none|ttl|manual", "revocable_by": "str"}
}
```

## Failure modes

- **Auditing the read path.** Reads are where the damage shows; writes are
  where it is decided.
- **Testing inside one session.** The property that matters is survival across
  identities and time.
- **Accepting a content filter as the control.** The record was written by your
  own summariser; it will not look like an attack.
