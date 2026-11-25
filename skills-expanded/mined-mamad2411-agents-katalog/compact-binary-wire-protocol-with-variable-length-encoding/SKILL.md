---
name: compact-binary-wire-protocol-with-variable-length-encoding
description: Define a custom binary wire format with variable-length integer encodings (e.g. 3-byte / 5-byte) to minimize UDP packet size for high-volume metric or telemetry streams
category: backend
version: 1.0.0
source_type: extracted-from-git
source_url: https://github.com/kjuhwa/scouter
source_ref: master
source_commit: 126bb19f07d1fe4fe915eb408c381e2c140cc94c
source_project: scouter
version_origin: extracted
tags: [protocol, binary, varint, udp, telemetry, perf]
confidence: high
---

# Compact Binary Wire Protocol with Variable-Length Encoding

Apply this when you're emitting high-frequency structured data (metrics, traces, events) over UDP or bandwidth-constrained links where standard 4/8-byte int/long is wasteful.

## Pattern

1. Choose type widths to match actual value domains:
   - Milliseconds / small counts → `INT3` (3 bytes, ≤ 16.7M).
   - Timestamps (epoch ms, 40 bits) → `LONG5` (5 bytes).
   - Fall back to 4/8-byte types when range is needed.
2. Reader and writer share a schema descriptor (field type list) — no type tags inline, saves per-record bytes but forces schema versioning.
3. Emit a short pack header (type byte + length) so readers can skip unknown pack types forward-compat.
4. Compress multi-record buffers (LZ4, snappy) at the *pack* layer, not per-field.

## Evidence

- `scouter.common/src/main/java/scouter/io/DataOutputX.java` — writer with writeInt3 / writeLong5
- `scouter.common/src/main/java/scouter/io/DataInputX.java` — reader
- `scouter.common/src/main/java/scouter/lang/pack/Pack.java` — pack envelope

## Trade-offs

- 20–40% size reduction on typical metric packs (scouter measurement).
- Requires coordinated schema evolution — mismatched reader/writer versions = silent corruption. Version your pack types.
- Hand-rolled wire format; less tooling vs. Protobuf / Flatbuffers. Justified only at very high packet volume.

## Related knowledge

- `variable-length-integer-encoding-for-metrics-bandwidth` (decision)
- `udp-for-throughput-tcp-for-reliability` (decision)
