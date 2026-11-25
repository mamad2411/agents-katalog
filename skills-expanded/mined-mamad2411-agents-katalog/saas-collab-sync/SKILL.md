---
name: saas-collab-sync
description: Realtime collaboration and sync specialist. Auto-invoked when realtime features are being built — WebSocket/SSE/long-polling protocols, CRDT/OT implementations, presence systems, conflict resolution, optimistic updates, or offline-replay patterns.
---

# SaaS Collab & Sync

Concurrent editing has to feel instant, survive disconnects, and converge
correctly — a sync layer that diverges produces corruption customers cannot
recover from, and it rarely shows up before production traffic.

## When to reach for this

- Choosing or implementing a realtime transport (WebSocket, SSE, long-polling)
- Adding CRDT/OT-based collaborative editing, presence, or live cursors
- Building optimistic UI updates, offline queues, or replay-on-reconnect
- Debugging divergence, dropped updates, or noisy-tenant fan-out problems

## Principles

1. **Pick the simplest transport that works.** SSE covers most server-push cases;
   reach for WebSocket only when bidirectional or low-latency input matters.
   Long-polling is a valid fallback, not a shame.
2. **Design for reconnection on day one.** Mobile networks drop constantly.
   Heartbeat at ~25–30 s (under typical 60 s proxy idle timeouts), reconnect with
   exponential backoff plus jitter, and resume from a server-assigned offset.
3. **Every op is tenant-scoped and authorized server-side, per-op.** A connected
   socket is not a license to mutate — connection-time auth alone is a leak.
4. **CRDTs over OT for greenfield.** Start with Yjs, Automerge, or Loro unless you
   specifically need server-authoritative edit control. Rolling your own OT is a
   multi-year project.
5. **Optimistic updates need a tested rollback path.** Apply locally, reconcile on
   server confirm/reject. The reject branch is where untested code corrupts state.
6. **Offline queue: durable, deduped, ordered.** Persist queued ops across client
   restart; dedupe on a stable client-generated op ID; replay in original order.
7. **State delivery semantics explicitly.** Most systems are at-least-once with
   idempotent application via op IDs — "exactly-once transport" is a design smell.
8. **Backpressure is not optional.** Per-connection and per-document rate limits;
   one chatty tenant must not degrade the shard.

## Transport decision table

| Situation | Transport | Notes |
|---|---|---|
| Server→client push only (notifications, dashboards) | SSE | auto-reconnect built in via `Last-Event-ID` |
| Bidirectional, low-latency input (co-editing, cursors) | WebSocket | own the heartbeat + resume protocol yourself |
| Restrictive corporate proxies / transport fallback | long-polling | keep the message schema identical to the primary transport |
| Occasional client→server writes alongside SSE | SSE + plain HTTP POST | often beats WebSocket for simplicity |

Whatever the transport: version the message schema from message one, and make
`resume(offset)` a first-class server operation — not a client-side full refetch.

## Pitfalls

- Authorizing only at connection time, then trusting every subsequent op
- Optimistic UI with no rollback — server rejection silently forks client state
- Offline queue in memory only; a tab crash loses user edits
- Presence updates fanned out unthrottled — typing indicators at keystroke rate
  melt the channel; coalesce to ~1 update/s per user
- Testing only on localhost — the real conditions are packet loss, reorder,
  duplicate delivery, multi-second latency, and client clock skew
- LWW conflict resolution applied to rich text or nested structures (it loses
  user data by design; reserve it for scalar fields)

---
*Related: `saas-multitenancy` (channel isolation, per-tenant limits),
`saas-data-model` (persisted sync state), `saas-auth-sso` (socket auth/session),
`api-design` (message contracts) · domain agent: `saas-architect` (realtime
topology) · output/ADR format: `playbook-conventions`*
