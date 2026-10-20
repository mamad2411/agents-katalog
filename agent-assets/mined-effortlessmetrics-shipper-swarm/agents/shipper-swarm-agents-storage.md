# AGENTS.md

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

# Module: `crate::ops::storage`

**Layer:** ops (layer 1, bottom)
**Single responsibility:** Storage backend trait + filesystem-backed implementation. Cloud backends (S3/GCS/Azure) are stubbed pending implementation.
**Was:** Runtime portion of the standalone `shipper-storage` crate (split during the decrating effort — config types went to `shipper-types::storage`).

## Public-to-crate API
- `StorageBackend` trait
- `FileStorage` (filesystem impl)
- `build_storage_backend` factory
- `config_from_env` (env-var parsing)

Re-exported for convenience: `CloudStorageConfig`, `StorageType` from `shipper_types::storage`.

## Invariants
- File backend: writes atomically via temp file + rename.
- S3/GCS/Azure: currently bail with "not yet implemented". Do not promise these to external users.
- The trait stays as a trait so future cloud backends can plug in.

## Why this lives inside `shipper-core`, not as a public crate
The trait + filesystem impl is mature, but the cloud backends are stubbed. Promising a public `StorageBackend` trait via crates.io would freeze a half-finished design. Keeping it internal lets us evolve until cloud backends are real. When cloud backends are implemented, this module can either be promoted to a public storage API surface or extracted into a new standalone crate.

