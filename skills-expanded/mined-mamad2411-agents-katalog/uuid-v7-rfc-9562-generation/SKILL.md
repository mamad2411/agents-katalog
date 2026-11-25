---
name: uuid-v7-rfc-9562-generation
description: Generate RFC 9562 compliant UUIDv7 with millisecond timestamp prefix for sortability
category: architecture
version: 1.0.0
version_origin: extracted
confidence: high
tags: [evolver, architecture, uuid, identifiers]
source_type: extracted-from-git
source_url: https://github.com/EvoMap/evolver.git
source_ref: main
source_commit: 22773782475cecf43dc9c1af264bf5f9cacc28bc
source_project: evolver
source_paths:
  - src/proxy/mailbox/store.js
imported_at: 2026-04-18T00:00:00Z
---

# UUIDv7 (RFC 9562) generator

UUIDv7 puts a 48-bit millisecond timestamp in the high bits, the version nibble in bits 48–51, and random bits everywhere else. IDs generated at different times sort lexicographically by time — ideal for append-only logs, outbox tables, and file naming.

## Mechanism

```js
function uuidv7() {
  const ms = Date.now();
  const hex = ms.toString(16).padStart(12, '0');
  const rnd = crypto.randomBytes(10);
  rnd[0] = (rnd[0] & 0x0f) | 0x70;       // version 7
  rnd[2] = (rnd[2] & 0x3f) | 0x80;       // variant 10
  const r = rnd.toString('hex');
  return `${hex.slice(0,8)}-${hex.slice(8,12)}-${r.slice(0,4)}-${r.slice(4,8)}-${r.slice(8,20)}`;
}
```

## When to reuse

- Message/event IDs where chronological sort matters.
- Replacing `ULID` or `Date.now()+nonce` ad-hoc schemes.
- Any ID space where a DB sequence is undesirable (distributed systems, file-based stores).
