---
name: data-streams
description: >
  Designs, writes and debugs Ditto Data Streams (preview), peer-to-peer topic streams
  outside document sync: bindTopic, connect, DittoStream,
  DittoAcceptor, candidates and take(), reliable vs unreliable topics,
  sendAndForget/maxSendSize, NGN (DITTO_NETWORK_ENABLE_NGN). Use for low-latency live
  data between peers or errors like "Failed to connect stream:
  Rejected(HandshakeTimedOut)" or "Err(InvalidTopic)". Kotlin/Swift syntax lives in
  those SDK skills. Not for document sync or attachments.

allowed-tools: Read, Grep, Glob, Edit, Write
---

# Ditto Data Streams

A Data Stream is a **low-latency, bidirectional, peer-to-peer channel of raw bytes**
between two reachable Ditto peers, opened on a named **topic**. Streams are ephemeral and
**never write to the Ditto store**: nothing is persisted, queried or converged. The app
defines its own wire format (Protobuf, JSON, raw frames). One peer **binds** a topic
(server role, gets an *acceptor*); another **connects** to it (client role); after that
both sides send and receive symmetrically
(<https://docs.ditto.live/sdk/latest/sync/data-streams>).

**Preview API, may change without notice.** Available in **Kotlin from 5.1.0** (Android and
JVM; the docs cover Android) with a per-file `@file:OptIn(com.ditto.kotlin.PreviewDataStreams::class)`,
and in **Swift from 5.2.0** only through `@_spi(PreviewDataStreams) import DittoSwift`
(not on 5.1.0; not in the Ditto docs). No other SDK documents it. State the preview
status and the version floor whenever you recommend it.

Read only the reference the task needs; per-language code is in
[`kotlin-sdk/references/data-streams.md`](../kotlin-sdk/references/data-streams.md) and
[`swift-sdk/references/data-streams.md`](../swift-sdk/references/data-streams.md).

## When to use streams, and when not

Use Data Streams for **real-time, high-frequency or ephemeral** bytes that one reachable
peer needs *now* and nobody needs later: sensor readings, telemetry, live cursor or stroke
previews, audio frames, RPC-style control messages. Use **document sync** (and
`sync-subscriptions`) when the data must persist, be queried with DQL, reach peers that
are offline now, or converge across the whole mesh; use an **attachment** for a large
blob that belongs to a document. Most apps use both: the whiteboard reference app streams
live strokes and ships committed operations over a reliable stream, while profiles stay in
documents.

"Point-to-point" is logical: NGN routes a stream through intermediate peers when the two
ends are not directly connected, but the *application* still talks to exactly one peer per
stream (<https://docs.ditto.live/sdk/latest/sync/data-streams>).

## The lifecycle, end to end

1. **Receiver binds** a topic with a reliability mode and **keeps the acceptor alive**.
   Only one acceptor per topic at a time (executed: a second bind fails).
2. **Sender discovers** the receiver's peer key through **presence** (sync must be
   running). Presence proves the peer is reachable, **not** that it has bound the topic.
3. **Sender connects** to that peer key on the topic, with the **same reliability**
   (mismatch is rejected: `Rejected(ConnectionRejected)`, executed).
4. **Receiver's bind callback fires** with a **candidate**. The candidate is valid only
   inside the callback: **open it there, or `take()` it** and close the taken one later.
   Use after the callback throws "Attempted to use a DittoStreamCandidate after it was
   closed" (executed).
5. **Sender's connect block receives a candidate** too; `connect` does **not** open it
   for you. Open it in the block (or `take()`), return the stream.
6. **Both send and receive.** The receive callback runs on the connection's **driver
   thread**: copy the payload out, hand it to a queue, return.
7. **Either side closes.** Closing the **acceptor unbinds the topic but does not close
   streams already open on it** (executed); close those yourself. A stream closed on one
   side reports `ClosedByRemote` on the other (executed).

Streams **never reconnect by themselves**. A closed stream stays closed until the app opens
a new one; expect early connects to fail while the other side is still starting, and retry
with bounded backoff (<https://docs.ditto.live/sdk/latest/sync/data-streams>).

## Reliability

| | Reliable | Unreliable |
|---|---|---|
| Delivery | in order, or the connection fails | may be lost, reordered, duplicated |
| Latency | higher | lowest |
| Compression | optional LZ4 (`requestCompression`) | not applicable |
| Use for | control messages, RPC, ordered file chunks, committed operations | frames superseded by the next one: audio, sensors, live cursors |

Neither mode is once-only; tolerate duplicates. `Sent` means "handed to the local
transport", not "the receiver's app processed it". Binder and connector must agree
(<https://docs.ditto.live/sdk/latest/sync/data-streams>).

## Sending

Check `maxSendSize` before every send; pick **one** send mode per message:
`send` (await a terminal `DittoSendStatus`: `Sent`, `Failed`, `Cancelled`; treat
`Unknown` as terminal too), `sendAndForget` (no status, least overhead, fits unreliable
frames), or `send` with a monitoring block (`currentStatus` / `awaitStatusChange`) for
backpressure. **Connect once and reuse the stream**; a connect per message defeats the
purpose and overlaps attempts (<https://docs.ditto.live/sdk/latest/sync/data-streams>).
Topics match `^[a-zA-Z0-9_ ]{1,15}$` (`Err(InvalidTopic)` otherwise, executed).

## Setup

Data Streams run over **NGN** (next-generation networking), which must be on **before the
instance is created**: the environment variable `DITTO_NETWORK_ENABLE_NGN=true` (Android
`Os.setenv` in `Application.onCreate()`; the process environment on the JVM), or on 5.2.0
`systemParameters = { ngn_data_streams_enabled: true, ngn_sync_enabled: false }` in the config. Keep
`replication_over_ngn` (`DITTO_REPLICATION_OVER_NGN`) **false** in the preview unless every
peer that must replicate sets the same value. Start sync so presence can discover peers.
**No TCP listener is required**; if you do change transports, modify the current config,
never a fresh one (every transport off). [setup-and-transports.md](references/setup-and-transports.md).

## Bring-up checklist

When nothing arrives, check in this order and stop at the first failure
([troubleshooting.md](references/troubleshooting.md) maps each error string to a cause):

```
- [ ] 1. NGN enabled on both peers before Ditto is created
- [ ] 2. Sync started on both peers; presence shows the remote peer
- [ ] 3. Receiver bound a valid topic (^[a-zA-Z0-9_ ]{1,15}$) and keeps the acceptor alive
- [ ] 4. Reliability matches between binding and connect
- [ ] 5. Candidate opened inside the callback, or take()n for later use
- [ ] 6. One stream reused per peer and topic; each payload under maxSendSize
```

## Anti-patterns

- Moving a candidate out of its callback without `take()`, or not closing a taken one.
- Expecting `connect` to open the candidate, or returning before opening it.
- Retaining the inbound message or send-operation wrapper beyond its callback.
- Blocking, decoding, database or UI work inside the receive callback.
- Assuming closing the acceptor closes its streams, or that a stream reconnects.
- `waitUntilClosed` used as if it closed anything; `closeSync`/`closeAndWait` does.
- Calling `connect` inside a presence callback; copy the key out and connect elsewhere.
- Per-message connects; mismatched reliability; a topic outside the pattern; a payload
  over `maxSendSize`; two acceptors on one topic; a fresh transport config.
- Treating reliable as "guaranteed" or once-only, or as a substitute for document sync.

## References

| If you need to know… | Read |
|---|---|
| Who owns which handle, and the shutdown order | [lifecycle-and-ownership.md](references/lifecycle-and-ownership.md) |
| Reliability, send statuses, backpressure, arguments, compression | [reliability-and-delivery.md](references/reliability-and-delivery.md) |
| NGN, replication over NGN, transports, presence, platform notes | [setup-and-transports.md](references/setup-and-transports.md) |
| An error string or a stream that never opens | [troubleshooting.md](references/troubleshooting.md) |
| Telemetry, whiteboard and push-to-talk designs | [patterns.md](examples/patterns.md) |
| Design rules before writing code | [best-practices.md](best-practices.md) |
| Kotlin code | [kotlin-sdk/references/data-streams.md](../kotlin-sdk/references/data-streams.md) |
| Swift code (5.2.0+) | [swift-sdk/references/data-streams.md](../swift-sdk/references/data-streams.md) |

## SDK 5.2.0 parameter names

For 5.2.0, prefer `ngn_data_streams_enabled = true` and `ngn_sync_enabled = false`
in `DittoConfig.systemParameters` before open. The older `network_enable_ngn` and
`replication_over_ngn` names used in pre-5.2 recipes remain deprecated aliases.
Enabling `ngn_sync_enabled` without `ngn_data_streams_enabled` now makes sync start
fail. Keep document sync on the legacy path unless the deployment deliberately enables
NGN sync on all required peers. This does not make Data Streams generally available;
the preview status and per-language gates still apply. Source: <https://docs.ditto.live/sdk/latest/release-notes-hub/swift> (5.2.0 common changes).
