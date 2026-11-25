---
name: couchbase-app-integration
description: "Build application code that integrates with Couchbase. Use whenever the user asks about Couchbase SDKs (Python, Java, Node.js, .NET, Go, C, Ruby, PHP, Scala, Kotlin), connection strings, connection pooling, async vs sync clients, retry strategies, timeout patterns, circuit breakers, durability levels, scan consistency, bulk / batch operations, application-side transactions, the transactions library, idempotency, write conflict handling, active-active XDCR application patterns, error categorization (transient vs durable), TLS / mTLS client setup, certificate handling in clients, or any 'how do I do X in the Couchbase SDK' question. Triggers on application-developer language distinct from couchbase-mcp (server operation), couchbase-data-modeling (database design), and couchbase-sizing (capacity). Use proactively for: integrating a new app, debugging client-side errors, choosing durability for a write, picking the right SDK pattern, handling XDCR conflicts at the application layer."
license: MIT
---

# Couchbase application integration

A skill for *building application code* that talks to Couchbase. Distinct from the three sibling skills:

- `couchbase-data-modeling` — what to store (server-side)
- `couchbase-sizing` — how much capacity (resource planning)
- `couchbase-mcp` — operations on an existing cluster (admin)
- **`couchbase-app-integration` (this skill)** — how application code reads, writes, and handles errors against Couchbase

If the conversation is "I'm writing Python (or Java, Node, etc.) code that talks to Couchbase," this is the right skill.

## When this skill applies

- "Which Couchbase SDK should I use?"
- "How do I set up the connection?"
- "What's the right way to handle retries?"
- "Should I use synchronous or asynchronous?"
- "What durability level for this write?"
- "Bulk inserting a million documents — how?"
- "Transactions in [language]?"
- "Active-active XDCR — how does my code handle conflicts?"
- "Why does my client get [error]?"

## Pick the right reference

| Question | Read |
|---|---|
| "Which SDK / which version / install how?" | `references/sdks.md` |
| "How do I connect — strings, TLS, mTLS, pooling, lifecycle?" | `references/connection-management.md` |
| "Retries, timeouts, circuit breakers, transient vs durable errors?" | `references/error-handling.md` |
| "Durability levels and scan consistency — what to pick?" | `references/durability-and-consistency.md` |
| "Bulk ops, async patterns, batching — making it fast?" | `references/performance-patterns.md` |
| "Multi-document transactions in code — when, how, gotchas?" | `references/transactions-app-side.md` |
| "Active-active XDCR conflicts — what does my app need to do?" | `references/xdcr-app-aware.md` |

## The four design questions for every Couchbase app

Before writing any client code, the answers to these four questions determine 80% of what the integration looks like:

1. **Sync or async?** Latency-sensitive request/response servers usually want async. Batch and ETL code can use sync. Mixing is fine but pick per-component.
2. **What durability is required?** From "best-effort" (lowest latency, no guarantees on power loss) up to "persist to majority" (slowest, durable through cluster-wide power loss). Most workloads want `Majority` — see `durability-and-consistency.md`.
3. **What's the consistency for reads?** Index-backed queries default to `NotBounded` (eventually consistent) which is fast but may miss recent writes. For read-your-own-writes patterns, use `RequestPlus`. See same reference.
4. **How does the code handle failure?** Cluster failovers, network blips, individual node restarts — the SDKs auto-handle most of this, but your retry/timeout policy determines whether outages are seamless or visible. See `error-handling.md`.

Get these four right and the rest is mostly typing.

## Three principles

**Principle 1 — Let the SDK do its job.**
Modern Couchbase SDKs handle connection pooling, failover routing, retry on transient errors, and load distribution automatically. Don't reimplement these. Wrap the SDK only when your application has needs the SDK doesn't cover (e.g., a circuit breaker on top of the SDK's retries).

**Principle 2 — Match the SDK's idioms.**
The Python SDK uses Pythonic patterns (`with`, context managers, type hints); the Java SDK uses reactive streams and CompletableFuture; the Node SDK uses promises. Code that fights the SDK's idioms is harder to maintain. Use what the SDK gives you.

**Principle 3 — Durability is per-operation, not per-app.**
You don't pick "the app's durability level." You pick per-write durability based on what's being written. Session updates: `None` or `Majority` is fine. Financial writes: `MajorityAndPersistActive` or `PersistToMajority`. Mix freely.

## Common shapes to recognize

| Application pattern | What the user usually needs |
|---|---|
| Web API / microservice with synchronous responses | Async SDK, connection pooling, request-level timeout, error categorization |
| Background worker / ETL | Sync SDK, bulk operations, longer timeouts, retry on transient |
| Real-time analytics dashboard | Async SDK, `RequestPlus` consistency on critical reads, `NotBounded` on others |
| Mobile sync gateway (Sync Gateway / App Services) | Different product entirely — out of scope here; refer user to Couchbase Mobile docs |
| Event-driven app reacting to mutations | Eventing functions (server-side, not SDK) — see `couchbase-mcp` skill |
| High-throughput bulk loader | Sync SDK with bulk APIs, defer index builds, parallelism per node count |
| Multi-region active-active | Application-level idempotency + conflict awareness — see `xdcr-app-aware.md` |

## What this skill won't help with

- **Server-side eventing functions** (which are JS code, but run on the cluster — see `couchbase-mcp` skill)
- **Cluster operations** (creating buckets, etc. — see `couchbase-mcp`)
- **Schema / document design** (see `couchbase-data-modeling`)
- **Capacity planning** (see `couchbase-sizing`)
- **Couchbase Mobile / Sync Gateway** (different product, not covered here)

Hand off explicitly when the conversation crosses these lines.

## A note on SDK versions

The Couchbase SDKs have had several major version transitions (SDK 2.x → 3.x → 4.x in Python, similar in others). Code patterns differ significantly between versions, and stale tutorials are everywhere on the internet. Always specify a version when the user asks about SDK usage — if they're on SDK 3.x patterns, code from SDK 2.x tutorials won't work.

When in doubt, point the user at the official SDK docs at https://docs.couchbase.com/<sdk-name>/current/ for current syntax.
