# Binary & Data Serialization

## Purpose
Implement deterministic, versioned binary and data serialization (Protobuf, MessagePack, JSON) with explicit schema evolution rules, canonical byte output, and fuzz-verified round-trip guarantees for caches, queues, and network protocols.

## Use when
- Defining Protobuf, FlatBuffers, MessagePack, or JSON schemas for APIs, events, cache payloads, or game packets.
- Enforcing deterministic canonical encoding so hashes, signatures, and snapshots are stable byte-for-byte.
- Evolving schemas with backward and forward compatibility across deployed producers and consumers.
- Diagnosing payload bloat, deserialization crashes, endianness bugs, or cross-language type mismatches.

## Do not use when
- Verifying HTTP consumer-driven contracts without changing wire formats (use `api-contract-testing`).
- Tuning page load or bundle size without touching encodings (use `performance-web`).
- Implementing lockstep or rollback netcode using already-fixed packet formats (use `realtime-synchronization`).

## Required context
- Schema sources: .proto files, MessagePack definitions, or JSON Schemas with version and owners.
- Compatibility matrix: deployed producer and consumer versions that must interoperate during rollout.
- Payload budgets: max bytes per message, target p99 encode/decode time in microseconds.
- Language runtimes involved (Go, Python, Rust, TypeScript) with their codegen plugins and versions.

## Procedure
1. **Model the schema explicitly**: define messages in Protobuf 3 with explicit field numbers, never reuse retired numbers, reserve deleted fields, document units (milliseconds, cents) in comments, and generate code with pinned protoc 26 plus language plugins.
2. **Guarantee deterministic canonical output**: sort map keys, use fixed field ordering, emit UTC timestamps as int64 epoch millis, and verify byte stability by encoding the golden fixture orders_golden_v3.bin twice and diffing SHA-256 hashes.
3. **Enforce schema evolution discipline**: additive optional fields only within a major schema version; never change a field number, wire type, or required semantics; validate with buf breaking and protovalidate rules before merge.
4. **Harden decoding**: reject unknown enum values with explicit UNRECOGNIZED handling, cap recursion depth at 32 and message size at 2 MB, validate UTF-8 on strings, and map decode failures to typed errors with message name and field path.
5. **Prove round-trip and cross-language parity**: run property-based fuzz over 100,000 random messages asserting decode(encode(m)) equals m, plus a cross-runtime corpus (Go encoder, Python decoder and reverse) with zero mismatches.
6. **Measure payload and speed**: benchmark against budgets (event envelope under 512 bytes p99, decode under 25 microseconds p99 on CI runner), record results, then execute scripts/verify.sh from the repo root.

## Decision rules
- **Deterministic bytes always**: identical logical messages must serialize to identical bytes; nondeterministic map iteration in encoders is a defect.
- **Never reuse field numbers**: retired numbers stay reserved forever; reuse corrupts rolling deployments silently.
- **Tolerant readers, careful writers**: readers ignore unknown fields and default missing ones; writers never emit ambiguous or redundant encodings.
- **Explicit endianness on custom formats**: hand-rolled binary layouts declare little-endian with magic bytes and version prefix; host-order assumptions are forbidden.
- **Budgets gate schemas**: messages exceeding the byte or microsecond budget are redesigned, not waived.

## Evidence required
- buf breaking report with zero breaking findings plus protovalidate lint log.
- Fuzz round-trip logs (100,000 cases) and cross-language corpus results with zero mismatches.
- Benchmark report against byte and microsecond budgets.
- Passing execution log from scripts/verify.sh.

## Output contract
- Versioned schema sources with codegen outputs, golden fixtures, and evolution notes.
- Deterministic encoder/decoder implementation with typed error mapping.
- Round-trip, parity, and benchmark evidence meeting the stated budgets.

## Stop conditions
- Schemas versioned, deterministic hashes stable, fuzz and parity green, budgets met.
- Incompatible deployed version discovered that forces a major schema version and migration plan.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to Lead Architect if a wire-incompatible change is unavoidable across fleets that cannot upgrade atomically.
- Escalate to Security if deserialization of untrusted input risks crashes, excessive allocation, or billion-laughs style expansion.
