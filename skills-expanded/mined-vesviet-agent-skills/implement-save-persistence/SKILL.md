---
name: implement-save-persistence
description: Implements monotonic save schemas, version migration pipelines, cryptographic integrity checksums, binary and JSON serialization, and cross-platform cloud saves. Use when building game save systems, profile persistence, autosave checkpoints, or Steam Cloud synchronization.
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - create_file
  - search_code
  - run_build
  - run_tests
  - run_linter
  - execute_command
version: "1.0.0"
---

# Implement Save Persistence

Architect and implement fault-tolerant game save and persistence systems with monotonic schema versioning, atomic disk writes, cryptographic integrity verification, and cross-platform cloud synchronization.

## Core Rules

- **Atomic Write-and-Swap Operations**: Never overwrite an existing save file directly in place. Always serialize to a temporary `.tmp` file, flush to disk (`fsync`), keep a rolling `.bak` backup of the previous valid save, and perform an atomic rename to the target save slot.
- **Monotonic Schema Versioning**: Embed an explicit integer `schema_version` in every save header. Maintain deterministic step-by-step migration functions (`v1 -> v2 -> v3`) so legacy player saves upgrade cleanly after patches.
- **Cryptographic Checksum Validation**: Compute and store a SHA-256 or HMAC-SHA256 digest of the serialized payload in the save envelope to detect corrupted writes, disk bit-rot, or malformed structures before deserialization.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` upon completing save persistence implementations.

## Suggested Process

### 1. Envelope & Monotonic Schema Design
Define a strict save envelope separating header metadata from game payload:
- Header: `magic_bytes`, `schema_version`, `timestamp_utc`, `playtime_seconds`, `payload_sha256`
- Payload: structured player progression, inventory state, world flags, and deterministic RNG seeds
Support human-readable JSON for debug builds and compact binary serialization (MessagePack, FlatBuffers, or binary streams) for production releases.

### 2. Version Migration Pipeline
Register sequential migration handlers indexed by source version. When loading a save where `file.schema_version` is older than `CURRENT_SCHEMA_VERSION`, iteratively apply each upgrade transform and validate invariants before hydrating runtime state.

### 3. Atomic Disk I/O & Corruption Recovery
Execute transactional file persistence:
- Write serialized bytes to `slot_0.sav.tmp` and verify byte count and SHA-256 digest.
- Copy existing `slot_0.sav` to `slot_0.sav.bak`, then atomically replace `slot_0.sav` with `slot_0.sav.tmp`.
- If primary save checksum verification fails on load, automatically fall back to `.bak` and alert the player safely.

### 4. Cross-Platform Cloud Save Synchronization
Store saves in OS-compliant user data directories (`user://`, `Application.persistentDataPath`) scoped by platform account ID. Integrate Steam Cloud Auto-Cloud or ISteamRemoteStorage APIs, resolving timestamp and playtime conflicts deterministically across devices.

## Output Contracts

When completing save persistence implementation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Save files write to a `.tmp` staging file and rotate a `.bak` backup before atomic rename
- [ ] Save header includes monotonic `schema_version` and verifies SHA-256 payload checksum on load
- [ ] Sequential version migration functions upgrade legacy save fixtures without data loss
- [ ] Serialization supports deterministic round-trip encoding in both binary and debug JSON formats
- [ ] Cloud save paths are scoped per account and handle multi-device sync conflicts safely
- [ ] Headless unit tests verify migration chains, checksum failure recovery, and round-trip integrity

## Failure Modes

- **Save corruption on interrupt**: a crash or power loss mid-write truncates the save being overwritten in place. Mitigation: serialize to a `.tmp` staging file, `fsync`, rotate a `.bak` of the previous valid save, then atomically rename into the slot.
- **Migration data loss**: a version jump (e.g. `v1 -> v3` directly) skips transform steps and silently drops legacy fields. Mitigation: apply sequential step-by-step migration functions (`v1 -> v2 -> v3`), validating invariants after each step against legacy save fixtures.
- **Checksum bypass**: a corrupted or malformed payload is deserialized before integrity verification and crashes the game on hydration. Mitigation: verify the SHA-256/HMAC-SHA256 envelope digest before deserialization; fall back to `.bak` and alert the player safely on failure.
- **Cloud sync clobber**: multi-device timestamp conflicts overwrite newer progress with an older cloud copy. Mitigation: resolve conflicts deterministically using timestamp plus `playtime_seconds`, scoped per platform account ID.
- **Schema drift without version bump**: new fields ship without incrementing `schema_version`, so older builds misparse newer saves. Mitigation: embed the integer `schema_version` in every header and fail closed on unknown newer versions.
- **Path traversal via slot/profile names**: user-supplied profile or slot names are concatenated into file paths, writing outside the save directory. Mitigation: sanitize names against a strict allowlist character set before path construction.
- **Autosave during critical sections**: an autosave fires mid scene-transition and snapshots a torn world state. Mitigation: trigger autosave checkpoints only at stable gameplay states.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: cloud save storage runs under the platform account identity. Mitigation: scope all read/write paths to the current account's directory (`user://`, `Application.persistentDataPath`, Steam Cloud); never touch another profile's slots.
- **ASI05 RCE Guard**: never deserialize saves with object deserializers that execute constructors or type callbacks. Mitigation: use data-only formats (JSON, MessagePack, FlatBuffers) validated against the schema after checksum verification.
- **ASI06 Context & Memory Poisoning**: saves are untrusted on-disk input; hex-edited inventories or world flags must not inject structure into runtime state. Mitigation: validate deserialized fields against schema types and ranges before hydrating gameplay systems.
- **ASI08 Cascading Failures**: checksum or migration failure must not propagate corrupt state into gameplay. Mitigation: declare the failure, fall back to `.bak`, and surface a safe player alert instead of continuing with partial data.
- **ASI07 Inter-Agent Communication**: save state is consumed by scene, engine, and narrative roles. Mitigation: emit the schema-valid `implementation-result.json` contract with schema version and storage layout so peers integrate against validated persistence.

## Related Skills

- **manage-scene-lifecycle**: hydrating and persisting scene state across level transitions
- **integrate-game-engine**: configuring platform user directories and headless test runners
- **integrate-dialogue-narrative**: persisting narrative condition flags and branching choices
- Companion reference: `references/versioned-save-schemas-and-checksums.md`
- Companion example: `examples/versioned-save-manager.ts`
