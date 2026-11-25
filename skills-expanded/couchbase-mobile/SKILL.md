---
name: couchbase-mobile
description: "Design and build mobile, edge, and offline-first applications with Couchbase Lite, Sync Gateway, and Capella App Services. Use whenever the user asks about Couchbase Lite, Sync Gateway, App Services, offline-first, mobile sync, data replication to mobile, Couchbase Lite database, replicator, push/pull replication, sync function, channel access, user authentication in mobile, conflict resolution in mobile, iOS Couchbase, Android Couchbase, React Native Couchbase, Xamarin Couchbase, .NET MAUI Couchbase, peer-to-peer sync, edge database, Couchbase Lite vector search, or 'how do I sync data to mobile apps.' Distinct from couchbase-xdcr (server-to-server replication) and couchbase-app-integration (server-side SDKs). Use proactively when the user has a mobile, IoT, field worker, or offline-capable application requirement."
license: MIT
---

# Couchbase Mobile

A skill for *designing and building* mobile and edge applications with Couchbase Lite + Sync Gateway / Capella App Services — offline-first sync, channel-based access control, conflict resolution, and mobile-specific patterns.

Distinct from:
- `couchbase-xdcr` — server-to-server replication between Couchbase clusters
- `couchbase-app-integration` — server-side SDK integration (Python, Java, Node.js, etc.)
- `couchbase-capella` — Capella cluster provisioning (App Services runs on top of a Capella cluster)

If the conversation is "I'm building a mobile app / offline-first app / IoT device that needs to sync with Couchbase," this is the right skill.

## When this skill applies

- "How do I sync data to an iOS / Android app?"
- "How do I build an offline-first app with Couchbase?"
- "What's Couchbase Lite?"
- "How does Sync Gateway work?"
- "How do I set up Capella App Services?"
- "How do I control which users see which documents?"
- "How do I handle conflicts in mobile sync?"
- "How do I do peer-to-peer sync between devices?"
- "Can I use vector search in Couchbase Lite?"

## Pick the right reference

| Question | Read |
|---|---|
| "Architecture — Lite vs Sync Gateway vs App Services, when to use which" | `references/architecture.md` |
| "Sync function — channels, access control, routing documents to users" | `references/sync-function.md` |
| "Couchbase Lite — replicator config, conflict resolution, queries" | `references/couchbase-lite.md` |

## Three core principles

**Principle 1 — Channel-based access is the security model.**
Sync Gateway / App Services control data access through channels. A document is routed to one or more channels by the sync function; a user has access to a set of channels. Users only receive documents in channels they have access to. There is no other row-level security mechanism — if you need per-document access control, you need per-document or per-group channels.

**Principle 2 — Offline-first means conflicts are inevitable.**
When two devices edit the same document while offline, both changes are valid locally. When they sync, a conflict occurs. Couchbase Lite resolves conflicts automatically (last-write-wins by default) or via a custom conflict resolver. Design your documents assuming conflicts will happen — use additive updates (event logs, append-only fields) over destructive in-place updates where possible.

**Principle 3 — The sync function runs on every document mutation.**
The sync function (or the equivalent access/channel routing in App Services) is a JavaScript function that executes on the Sync Gateway / App Services side for every document write. It determines which channels the document belongs to and who can read/write it. Keep it fast and free of side effects. Slow sync functions bottleneck the entire write path.

## Platform support

Couchbase Lite runs on:
- iOS (Swift, Objective-C)
- Android (Kotlin, Java)
- React Native
- .NET (Xamarin, .NET MAUI, Windows, macOS, Linux)
- Flutter (community)
- JavaScript / Ionic / Capacitor

All platforms share the same replication protocol and sync semantics. The API differs by language but the concepts are identical.

## Current releases (mid-2026)

The June 30, 2026 edge/mobile wave (shipped alongside the AI Data Plane — see `couchbase-ai-applications`) advanced the whole mobile stack. Gate version-specific guidance accordingly, and verify exact API surface against the docs for the version you target:

- **Couchbase Lite 4.1** — peer-to-peer sync over Bluetooth with automatic switch to Wi-Fi; expanded Windows / ARM support; on-device vector search continues from 3.2 (see `references/couchbase-lite.md`).
- **Edge Server 1.1** — client-level (per-client) access control; expanded Windows/ARM support. Edge Server is the lightweight on-prem/edge sync+query tier between Lite devices and the cloud.
- **Sync Gateway 4.1** — cloud-to-edge sync, non-disruptive rolling upgrades, concurrent distributed resync for high-volume workloads; available as a managed service through App Services.
- **React Native 1.1** — Turbo Module integration for direct Couchbase Lite performance without bridging overhead.

Don't remove older-version guidance when relying on these — mixed fleets are common in the field. Treat specific new API signatures as unverified until confirmed against the versioned docs.

## Capella App Services vs self-managed Sync Gateway

| | Capella App Services | Self-managed Sync Gateway |
|---|---|---|
| Management | Fully managed by Couchbase | You manage the install and config |
| Setup time | Minutes | Hours to days |
| Scaling | Automatic | Manual (add nodes) |
| Pricing | Included in Capella tier | License fee |
| Customization | Sync function via UI/API | Full config file control |
| Use when | Capella cluster; minimal ops overhead | On-prem; specific config requirements |

For new projects on Capella: use App Services. For self-managed Couchbase Server: use Sync Gateway.

## Related skills

- `couchbase-capella` — provisioning the Capella cluster that App Services connects to
- `couchbase-data-modeling` — document design decisions (especially channel design and conflict-resistant document shapes)
- `couchbase-security-hardening` — Sync Gateway TLS and authentication configuration
