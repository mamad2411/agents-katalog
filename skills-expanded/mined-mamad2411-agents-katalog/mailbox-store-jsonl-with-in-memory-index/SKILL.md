---
name: mailbox-store-jsonl-with-in-memory-index
description: Append-only JSONL persistence with in-memory index for fast message lookup and ordering
category: data-pipeline
version: 1.0.0
version_origin: extracted
confidence: high
tags: [evolver, data-pipeline, jsonl, mailbox, indexing]
source_type: extracted-from-git
source_url: https://github.com/EvoMap/evolver.git
source_ref: main
source_commit: 22773782475cecf43dc9c1af264bf5f9cacc28bc
source_project: evolver
source_paths:
  - src/proxy/mailbox/store.js
imported_at: 2026-04-18T00:00:00Z
---

# JSONL mailbox with in-memory index

Use a JSONL file (one JSON object per line) as the durable append-only log, and maintain in-memory indexes (Map for ID lookup, arrays for ordered inbound/outbound refs) rebuilt on startup.

## Mechanism

- Append: `fs.appendFileSync(path, JSON.stringify(msg) + '\n')` then `index.set(msg.id, msg)`.
- Load: read file line-by-line, `JSON.parse` each, populate index. Skip malformed lines with a warning.
- Schema evolve: include a `schema_version` on each record; migrate in a single pass when rebuilding the index.
- Separate volatile state (cursors, ack marks) into a side JSON file so the log stays append-only.

## When to reuse

- Local message queues, outbox patterns, event logs that must survive restart.
- Systems that want human-inspectable storage (grep, tail) without a database.
- Anywhere you need durable writes + fast lookup without SQLite/LMDB.
