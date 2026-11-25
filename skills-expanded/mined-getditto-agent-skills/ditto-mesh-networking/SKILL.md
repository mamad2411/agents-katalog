---
name: ditto-mesh-networking
description: >
  Use ONLY for Ditto peer-to-peer networking, not Zigbee, Thread, BLE Mesh, router
  mesh or service mesh. Chooses and configures Ditto transports (BLE, LAN, AWDL, Wi-Fi
  Aware, WebSocket, TCP), diagnoses discovery and connection failures, and sizes
  multihop sync, connection budgets and BLE documents. Use when devices don't discover
  each other or keep disconnecting, sync must work without Wi-Fi or internet, or
  transports are configured at runtime. Per-language syntax belongs to the Ditto SDK
  skill.

allowed-tools: Read, Grep, Glob, Edit, Write
---

# Ditto Mesh Networking and Transports

Ditto peers form a mesh over several transports at once. Each discovers peers and
opens physical connections; the multiplexer combines links to the same peer into one
virtual connection and selects a path for traffic (the rainbow connection). Presence
and multihop routing let peers sync without a direct connection or a server.

For 5.2.0 connection limits, keepalive defaults, wireless fixes and NGN settings, read
[versions.md](references/versions.md#sdk-520). Knowledge baseline: **5.2.0**; check release notes for anything newer.

## When this skill applies

- "Two devices never see each other" or "it syncs on Wi-Fi but not offline."
- "Which transports should a mixed iOS/Android fleet use without an access point?"
- "Can we change transports while the app is running?"
- "It connects, but sync over Bluetooth is very slow."
- Transport-condition callbacks, Local Network prompts, `NSBonjourServices`, Wi-Fi Aware
  or Android Bluetooth permissions.

## Diagnosis workflow

Copy this checklist when peers do not connect or data does not arrive:

```
- [ ] 1. Effective transport config logged on both peers (read-modify-write, not a fresh config)
- [ ] 2. Platform support, radio toggles, granted permissions and plist/manifest entries checked
- [ ] 3. Identity valid (an invalid certificate silently zeroes every P2P transport)
- [ ] 4. Failing stage located: discovery → connection → presence → subscription → replication → local query
- [ ] 5. One change applied, then re-observed from both peers over a time window
```

The full order is in [platform-requirements.md §8](references/platform-requirements.md#8-diagnosis-order).
"Sync active" is engine status, not proof of connectivity; change one setting at a time
and check both peers again before changing the next.

## Start with the task

Read only the matching reference section. Inspect the contents of a long file before
reading a section; do not load every reference or the README as setup.

| Task | Read |
|---|---|
| Diagnose missing peers or no sync | [platform-requirements.md §8](references/platform-requirements.md#8-diagnosis-order), then the failing stage in [mesh-formation.md §1](references/mesh-formation.md#1-the-six-stages-of-a-sync) |
| Choose radios, compare bandwidth/platforms/failure modes | [transports.md](references/transports.md), only the candidate transports |
| Cross subnets or bypass blocked mDNS | [transports.md §6](references/transports.md#6-explicit-tcp-connect-and-listen) |
| Set fields/defaults or change a running config | [transport-config.md](references/transport-config.md) |
| Understand presence, connection caps, churn or sync groups | [mesh-formation.md](references/mesh-formation.md) |
| Configure permissions, entitlements or OS/network prerequisites | [platform-requirements.md](references/platform-requirements.md), target platform only |
| Check a version or SDK-specific behavior | [versions.md](references/versions.md) |
| Budget documents/attachments/subscriptions for transports | [best-practices.md](best-practices.md) |
| Adapt a deployment | [deployment-scenarios.md](examples/deployment-scenarios.md), matching scenario only |
| Configure transport system queries | [transport-config.md §7](references/transport-config.md#7-transport-settings-that-live-in-dql-not-in-the-config-object) |

For exact API spelling, use the language's Ditto SDK skill or
<https://docs.ditto.live/sdk/latest/sync/customizing-transport-configurations>.
For query syntax use `write-dql`; for subscription propagation use `sync-subscriptions`;
for schema design use `data-modeling`. These are separate skills, not prerequisites.

## Version awareness

Supports Ditto SDK **4.14.x (LTS), 5.0.x, 5.1.x and 5.2.0**. Confirm the SDK when a claim
turns on version or platform: hard document-limit behavior, transport availability and
`TRANSPORTS_DISCOVERED_PEERS` (4.12.0+) are not universal. Consult the matching row in
`references/versions.md`; defaults are not a permanent contract.

## Choose a transport mix

| Transport | Reach and role | Platform constraint |
|---|---|---|
| Bluetooth LE | Nearby, infrastructure-free fallback; roughly 20 KB/s effective | Bridges native iOS and Android |
| LAN | Same Wi-Fi/Ethernet network; mDNS discovery + TCP; high bandwidth | Cross-platform; network may block multicast |
| AWDL | Fast nearby Apple-to-Apple sync without an AP | Apple only; check SDK/platform version |
| Wi-Fi Aware | Fast nearby Android-to-Android sync without an AP | Android API 29+; hardware support required |
| WebSocket | Known endpoint, usually Ditto Server; cloud store-and-forward | Only transport for browser/Wasm |
| TCP connect/listen | Known address/port; fixed infrastructure or blocked mDNS | Cross-platform native |

A mixed iOS/Android fleet without infrastructure depends on BLE: AWDL and Wi-Fi Aware
do not interoperate. WebSocket does not discover nearby peers. A small-peer-only mesh
works without Ditto Server but lacks cloud store-and-forward for peers never co-located.
Browser/Wasm rejects P2P settings; on native, unsupported-platform settings may throw or
be ignored depending on SDK. Validate platform prerequisites as well as configuration.

## Change configuration safely

The core config groups are `peerToPeer` (radios), `connect` (outbound endpoints),
`listen` (inbound listeners) and `global` (sync group/routing hint).

**Read-modify-write the current config. A freshly constructed TransportConfig starts
with every transport disabled**, unlike the platform defaults: setting only BLE can
silently turn off LAN and AWDL.

Runtime updates diff old/new config per transport:

- Enabling starts discovery/connections; disabling drops that transport's connections.
  Unchanged transports keep their connections. Ordinary changes need no sync restart.
- Added URLs start connection attempts. Removing URLs stops that endpoint only if a
  managed cloud URL is not being re-added by the SDK.
- **Stop sync before changing `syncGroup`, then start again.** A live change forces an
  internal restart. Sync groups scope connections; they are not an access-control boundary.
- Transport changes preserve local writes. Interrupted transfers resume; a received
  document stays invisible until complete. Enabling config cannot override OS radio
  state or a missing permission; inspect transport-condition callbacks.

## Size for the required radios

BLE's bandwidth makes many small documents preferable to a few large ones when BLE is
required. Documents appear only after complete arrival; 256 KiB takes over 10 seconds
at roughly 20 KB/s. Sync sends changed fields, but merge/storage work scales with the
whole document. On LAN/cloud-only fleets, embedding related data can remain appropriate.

The default soft warning is **256 KiB**, hard limit **5 MiB**. Whether oversized local
writes are rejected or only logged is version-dependent; check `references/versions.md`
before advising. 5.2.0 drops replication diffs that would push the document over its hard limit and stops that document’s updates until
eviction/re-sync; older versions can accept oversized replicated documents. Binary data belongs
in attachments, fetched separately by default. Use `data-modeling` for split decisions
and `best-practices.md` for transport budget calculations.

## Diagnose reachability over time

Peers intentionally do not all connect to every other peer. Connection budgets rank
**LAN > P2P Wi-Fi > BLE**, with release-dependent counts; churn frees slots for waiting
peers and helps prevent isolated islands. Direct edges change by design, so observe
reachability over a window. A missing direct connection alone is not a sync failure.

For missing data, locate the failing stage: discovery → connection → presence →
subscription → replication → local query. A relay can forward only data it holds;
see `sync-subscriptions` or <https://docs.ditto.live/key-concepts/syncing-data>.
Do not disable radios for battery savings without measurement: removing a fast path can
force more traffic over a slower, more expensive one.
