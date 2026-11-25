---
name: athena-storage
description: Athena storage module playbook for managed file catalog work, S3 catalog and credential changes, storage auth flows, presigned upload and download routes, storage OpenAPI docs, and canonical storage SQL artifacts in the Athena repo. Use when implementing or debugging `/storage/*` routes, `src/api/storage/**`, `src/api/s3.rs`, `crates/athena-s3/**`, `sql/files/athena-files.sql`, or Athena JS storage backend contracts that depend on this server behavior. Use when the user runs /athena-storage.
---

# Athena Storage

Work from the exact route, handler, or storage contract first. Prefer the current repo source and generated artifacts in this checkout over older docs or memory.

Current repo target: `athena_rs 3.20.0`.

## Source of truth order

Read in this order:

1. `docs/architecture/storage-files-schema.md`
2. `src/api/storage/auth.rs`
3. `src/api/storage/files.rs`
4. `src/api/storage/mod.rs`
5. `src/api/s3.rs`
6. `crates/athena-s3/src/{managed_files,file_catalog,store,schema,sql}.rs`
7. `sql/files/athena-files.sql`, `scripts/generate_storage_files_artifacts.py`, `sql/provision_files.sql`, and the generated storage block inside `sql/provision.sql`
8. `openapi.yaml` and the storage docs under `apps/docs/content/docs/reference/athena-openapi/storage/`

If docs and source disagree, prefer the current source, tests, and generated artifacts in this checkout.

## Pick the surface first

Managed file catalog surface:

- Use for `/storage/files*`, `/storage/folders*`, `/storage/permissions*`, `/storage/multipart*`, and `/storage/audit/list`.
- Route registration lives in `src/api/storage/files.rs`.
- Auth normally flows through `require_storage_actor` or `resolve_optional_storage_actor`.
- Durable catalog behavior lives mostly in `crates/athena-s3/src/managed_files.rs`.

Raw object and bucket utility surface:

- Use for `/storage/objects*` and `/storage/buckets*`.
- HTTP handlers live in `src/api/storage/mod.rs`.
- These routes operate closer to direct S3-compatible behavior and only bridge into managed catalog helpers when the route explicitly does so.

S3 catalog and credential admin surface:

- Use for `/storage/catalogs*` and `/storage/credentials`.
- HTTP handlers live in `src/api/s3.rs`.
- Durable catalog and secret-storage behavior live in `crates/athena-s3/src/store.rs`.

Schema and provision artifacts:

- Use `sql/files/athena-files.sql` as the canonical clean-install DDL.
- Use `crates/athena-s3/src/schema.rs` for additive runtime self-heal of existing installs.
- Do not patch only `sql/provision_files.sql` or only the generated block inside `sql/provision.sql`.

## Change workflow

1. Identify the exact route, path, or file contract.
2. Trace route registration in `src/api/storage/files.rs`, `src/api/storage/mod.rs`, or `src/api/s3.rs` before editing lower layers.
3. Trace auth and client pool resolution next:
   - managed file routes: `src/api/storage/auth.rs` plus `required_client_pool`
   - admin catalog routes: `authorize_static_admin_key` plus `required_client_pool`
4. Change the owning runtime layer instead of adding wrappers:
   - request parsing and HTTP envelope: `src/api/storage/**`
   - durable file catalog and permissions: `crates/athena-s3/src/managed_files.rs`
   - S3 catalog and encrypted credentials: `crates/athena-s3/src/store.rs`
   - storage object audit bridge: `crates/athena-s3/src/file_catalog.rs`
5. If the schema contract changes, edit `sql/files/athena-files.sql`, regenerate artifacts, and then align `crates/athena-s3/src/schema.rs` if existing installs need self-heal coverage.
6. If a public route contract changes, update `openapi.yaml` and any generated docs that mirror that path.

## Guardrails that matter

Preserve the split between managed files and raw object utilities. Do not move `/storage/files*` behavior into `src/api/storage/mod.rs` or bypass `athena-s3` helpers for managed catalog mutations.

Preserve the auth order in `src/api/storage/auth.rs`:

- static admin key
- Athena Auth session token or cookie
- bearer token lookup
- optional legacy identity headers only when explicitly enabled

Prefer additive schema changes. New tables or columns belong in repo SQL under `sql/` and must be reflected in the canonical DDL, not invented only inside runtime code.

Use the repo conventions:

- JS callers should use `@xylex-group/athena` rather than custom DB drivers.
- **Edge R2 L3a** (`createClient({ storage: { r2 } })` / putObject-getObject) is **not** the managed catalog HTTP surface. Route edge object-binding work to `$athena-js-cloudflare-edge-adapter`. This skill owns server `/storage/*` + athena-s3 catalog contracts.
- Rust validation should run through WSL2, not native Windows `cargo test`.

Read [references/storage-seams.md](references/storage-seams.md) when you need the file ownership map, schema-generation chain, or existing storage-focused tests.

## Validation

Prefer the narrowest proof that matches the seam you changed.

Schema and generated-artifact checks:

```powershell
python scripts/generate_storage_files_artifacts.py --check
```

If the canonical DDL changed, regenerate before validating:

```powershell
python scripts/generate_storage_files_artifacts.py
```

Focused Rust validation in WSL2:

```powershell
wsl.exe bash -lc 'cd /mnt/c/Users/floris/Documents/GitHub/athena && cargo test -p athena-s3'
wsl.exe bash -lc 'cd /mnt/c/Users/floris/Documents/GitHub/athena && cargo test --test auth_hardening storage_ -- --nocapture'
wsl.exe bash -lc 'cd /mnt/c/Users/floris/Documents/GitHub/athena && cargo test --test openapi storage_ -- --nocapture'
```

Add broader validation only when the change crosses into provisioning, gateway routing, or other subsystems.
