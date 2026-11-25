---
name: offline-first-sync
description: Designs local storage and background sync with conflict handling, so an app stays usable on flaky networks and never silently loses edits.
---

# Offline first sync

The local database is the source of truth for the UI. The network is a background job.

## Steps

1. Inventory the data. For each entity record: who edits it, how often, whether concurrent edits are realistic, and whether deleting matters. Ask the user only for facts the code cannot answer.
2. Choose a conflict rule per entity, not one rule for all. Last-write-wins on a server timestamp suits settings. Field-level merge suits profiles. Append-only suits messages and logs. Explicit user resolution suits documents. State the choice and its cost.
3. Local schema. Every synced row gets a client-generated id (UUIDv7 or ULID), `updatedAt`, a `version` or server revision, a `deletedAt` tombstone instead of hard delete, and a `syncState` of `synced`, `pending` or `conflict`.
4. Write path. UI writes to the local store and appends an operation to an outbox in one transaction. The outbox entry holds an idempotency key, entity, operation and payload.
5. Sync loop. Push the outbox in order, sending the idempotency key so the server ignores repeats. On success mark rows synced. Then pull changes since the last cursor, apply them in a transaction, and advance the cursor only after commit. Retry with exponential backoff and jitter. Trigger on connectivity change, app foreground and a periodic job.
6. Conflicts. On a version mismatch the server answers with its copy. Apply the entity's rule. Never discard the losing change without keeping it somewhere the user or a log can recover.
7. Tests: airplane-mode edit then reconnect, same edit sent twice, two clients editing one field, a crash between push and cursor save, and a deleted record edited elsewhere.

## Rules

- Never use auto-increment ids generated on the server for rows created offline.
- Never show a spinner for data already stored locally.

## Report

The conflict rule per entity, schema changes, and which failure tests pass.
