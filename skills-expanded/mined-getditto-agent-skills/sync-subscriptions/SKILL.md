---
name: sync-subscriptions
description: >
  Designs and debugs Ditto sync subscriptions (registerSubscription): which SELECT
  queries a subscription accepts, why documents are missing on a peer, receive-side
  filtering, multihop relay coverage, flooding, persistence and cancellation. Covers
  SDK 4.14.x, 5.0.x, 5.1.x and 5.2.0. Use when data written on one device never
  arrives on another, a subscription query is rejected, or a relay forwards less than
  expected. Language-agnostic; API syntax belongs to the Ditto SDK skill.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Ditto Sync Subscriptions

A subscription declares **what this peer wants other peers to send it**. It copies
matching documents into the local store; a store query/observer reads that store.
Production apps typically need both. This skill owns subscription semantics, not
per-language `registerSubscription` spelling or local DQL query syntax.

Supports **Ditto SDK 4.14.x (LTS), 5.0.x, 5.1.x and 5.2.0**. Confirm the target version before
using version-sensitive clauses.

For 5.2.0 diagnostics and document-size enforcement during replication, read
[how-subscriptions-work.md](references/how-subscriptions-work.md#sdk-520-diagnostics-and-behavior).

## When this skill applies

- "Data written on one device never shows up on another."
- "`registerSubscription` throws `Unsupported feature: …`."
- "A relay device forwards only some of the documents."
- "After a restart, new documents stop arriving."
- Choosing between a subscription and a local query/observer, or narrowing what syncs.

## Start with the task

Read only the matching reference or section; do not read every file or the README.
Use the language's Ditto SDK skill for calls and `write-dql` for local queries.
If those skills are unavailable, use the official links below.

| Task | Read |
|---|---|
| Lifecycle, deltas, dedup/refcounting, cancellation, attachment behavior | [how-subscriptions-work.md](references/how-subscriptions-work.md) |
| A rejected query or exact version-specific restrictions/errors | [query-limitations.md](references/query-limitations.md) |
| Missing data across a relay, pairwise sessions or flooding | [mesh-and-flooding.md](references/mesh-and-flooding.md) |
| Work through a topology | [mesh-scenarios.md](examples/mesh-scenarios.md), matching scenario only |
| Design stable production subscriptions | [best-practices.md](best-practices.md) |

## Query rules

Start with `SELECT * FROM collection WHERE ...`: subscriptions sync whole documents,
not projections. The supported subset differs from local store queries.

- `SELECT *` is required. Projections, JOINs, multiple collections, `USE IDS`,
  `DISTINCT`, grouping/aggregates and non-SELECT statements are rejected.
- `WHERE` filters one collection. `USE INDEX`/planner directives are accepted.
- **4.14.x:** `LIMIT`/`ORDER BY` are accepted but stateful and discouraged.
  **5.x:** rejected by default. `OFFSET` alone is accepted on all supported lines.
- To sync only some fields, split the collection or move binary data to attachments.
  Filter/sort a view with a local store query rather than repeatedly replacing a
  subscription for each view change.

Exact error strings and the reasons for the restrictions are in
`references/query-limitations.md`; read it when constructing or debugging a query.

## Lifetime and local storage

- Subscriptions filter incoming data. Local writes land in the local store regardless
  of subscriptions; local queries can read everything stored locally.
- Registrations are in memory: re-register at each app start. Previously synced
  documents survive native app restarts; browser JS storage is in memory only.
- A document that stops matching gets one final update and remains in the store.
  Removal is explicit: `EVICT` is local; `DELETE` writes a replicating tombstone.
- Attachments normally sync a token, with bytes explicitly fetched.
  `ALTER SYSTEM SET attachments_auto_fetch = true` enables automatic fetching.
- Handle teardown is SDK-specific. In C++ and Rust, dropping a handle does not cancel
  its subscription: call `cancel()`. Check the language SDK guidance for ownership.

## Trace every hop for missing data

Default sync sessions are pairwise (5.1's opt-in multicast beta is a separate mode).
Two rules explain the relay bottleneck:

1. A peer offers documents it **holds**, filtered by the **recipient's subscriptions**.
2. A peer holds its own writes plus documents received through its own subscriptions.

If A holds all cars, B subscribes only to blue cars, and C wants all cars but connects
only through B, C receives only blue cars. B cannot relay the other cars it never
received. Sync is transitive with no hop limit, but relays are not transparent pipes.
A new path to a holder can fill the gap. Audit subscriptions and holdings at every
hop before changing the endpoints' queries.

Copy this checklist when documents are missing on a peer:

```
- [ ] 1. Subscription registered at this app start, and registration did not throw
- [ ] 2. Query fits the subscription subset for the target version (SELECT *, one collection)
- [ ] 3. Every hop on the path subscribes to, and so holds, the missing documents
- [ ] 4. A holder is reachable (presence shows a path) and permissions allow delivery
- [ ] 5. The local query or observer actually selects the synced documents
```

Ditto Server follows the same receive-filter and permission rules. A cloud path fills
the gap only if the server holds the missing documents and can serve them to C;
cloud connectivity alone does not establish complete data coverage.

## Official references

- [Syncing Data](https://docs.ditto.live/key-concepts/syncing-data): concepts.
- [Managing Subscriptions](https://docs.ditto.live/sdk/latest/sync/syncing-data): SDK calls.
- [Sync Handling](https://docs.ditto.live/best-practices/sync-handling): operations.
- [Stateful Subscription Performance](https://docs.ditto.live/stateful-subscriptions): LIMIT/ORDER BY costs.
