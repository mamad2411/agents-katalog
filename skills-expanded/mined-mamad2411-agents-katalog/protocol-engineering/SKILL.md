---
name: protocol-engineering
domain: engineering
level: engineering
description: Domain-agnostic method for framing, buffering, timeouts, checksums, and endianness — the recurring pitfalls of any binary or line protocol over any transport.
tags: [framing, checksum, crc, endianness, "binary protocol"]
triggers: [framing, checksum, crc, endianness, "binary protocol", "protocol design"]
version: "1.0.0"
requires: []
recommends: []
capabilities: []
conflicts: []
when_to_use: Designing, implementing, or debugging any protocol — binary or text — over any
  transport (serial, TCP, a message queue, a file format even). The method here is about the
  protocol layer itself, independent of which transport carries it.
when_not_to_use: A specific existing protocol whose behavior is already fully documented by a
  vendor/standard (e.g. HTTP, Modbus) — use that protocol's own skill/spec first; this is for
  the underlying method, not a substitute for protocol-specific documentation.
---

# Skill: protocol-engineering

## Purpose

The failure modes that recur across almost every hand-rolled or vendor binary protocol,
independent of transport — this is the method, not any one protocol's specifics.

## Method

1. **Transport delivers bytes; protocol gives them meaning — keep the two separated in code.**
   A transport (serial, TCP, USB) has its own delivery guarantees (or lack thereof); a protocol
   defines message boundaries and semantics on top. Code that assumes "one write on the sender
   equals one read on the receiver" conflates the two — this is almost never true for a stream
   transport (TCP, most serial APIs).
2. **Framing defines where one message ends and the next begins**, and there are exactly a few
   real strategies: a fixed length, a length prefix, a delimiter (with escaping for the
   delimiter byte appearing in payload data), or a sentinel start/end pair. Pick one
   deliberately and document it — an ad-hoc "read until it looks done" framing strategy is a
   reliable source of intermittent corruption once messages get split across reads.
3. **A partial read is the normal case, not an edge case.** `read()`/`recv()` on a stream
   transport can return fewer bytes than requested for entirely mundane reasons (OS buffering,
   packet boundaries, serial driver chunking) — always buffer and accumulate until a complete
   frame (per your framing strategy) is available, never assume one read call yields one
   message.
4. **Timeouts need two different answers: "how long to wait for more data" and "how long to
   wait for a full message."** Conflating them either times out mid-message on a slow but
   healthy link, or hangs forever on a link that stopped sending mid-frame. Decide both
   explicitly.
5. **A checksum/CRC only protects against what it's actually computed over.** Verify whether it
   covers the header, the payload, or both, and at what point in the pipeline (before or after
   any escaping/encoding) — a checksum computed pre-escaping and verified post-escaping (or vice
   versa) will fail non-deterministically depending on payload content.
6. **Endianness is a per-field decision, not a per-protocol given.** Don't assume every
   multi-byte field in a protocol uses the same byte order — some real-world protocols mix
   big-endian headers with little-endian payloads (or vice versa) for historical reasons; verify
   per field against the actual spec/capture, not by pattern-matching the rest of the protocol.
7. **Retries need idempotency or a sequence/ack scheme to be safe** — blindly retrying a
   non-idempotent command (an increment, an append) on a suspected-but-unconfirmed failure can
   apply it twice. If retries matter, the protocol needs some way to detect a duplicate.
8. **Capture, then replay, before touching code.** For nearly any protocol bug, a real captured
   byte sequence (verified against known-good behavior, from a working reference implementation
   or vendor tool) is a far more trustworthy source of truth than a spec sheet — specs
   frequently have transcription errors or ambiguity a real capture resolves immediately.
9. **Track device/connection state explicitly**, not implicitly through "whatever the last
   response implied" — a protocol that has modes, sessions, or sequence numbers needs its state
   tracked in code as its own explicit value, not inferred fresh from each response.

## Anti-patterns

- Assuming one `write()`/`read()` call corresponds to exactly one protocol message.
- Verifying a checksum against the wrong stage of the pipeline (pre- vs. post-escaping) and
  treating the resulting non-deterministic failures as a hardware problem.
- Retrying a non-idempotent operation on a timeout without a way to detect if it already
  succeeded.
