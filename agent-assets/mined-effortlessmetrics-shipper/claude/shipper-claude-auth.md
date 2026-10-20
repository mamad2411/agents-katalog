# Module: `crate::ops::auth`

**Layer:** ops (layer 1, bottom)
**Single responsibility:** Cargo registry token resolution.
**Was:** standalone crate `shipper-auth` + the in-tree shim with credential fallback (absorbed during the decrating effort; the dedup intermediate was PR #51).

## Resolution order
1. `CARGO_REGISTRY_TOKEN` env var
2. `CARGO_REGISTRIES_<NAME>_TOKEN` env var
3. `$CARGO_HOME/credentials.toml` (with crates.io aliases: `crates-io`, `crates.io`, `crates_io`, nested `[registries.crates.io]`)
4. Legacy `$CARGO_HOME/credentials` file

## Public-to-crate API (via `pub use` in `mod.rs`)
- `resolve_token(&str) -> Result<Option<String>>` — canonical top-level entry
- `detect_auth_type(&str) -> Result<Option<AuthType>>`
- `detect_auth_type_from_token(Option<&str>) -> Option<AuthType>` (pub(crate))
- `resolve_auth_info(&str, Option<&Path>) -> AuthInfo` — diagnostic record form
- `has_token`, `mask_token`, `cargo_home_path`
- `is_trusted_publishing_available()`
- `list_configured_registries(&Path) -> Result<Vec<String>>`
- `AuthInfo`, `TokenSource`
- Constants: `CRATES_IO_REGISTRY`, `CARGO_REGISTRY_TOKEN_ENV`, `CARGO_REGISTRIES_TOKEN_PREFIX`, `CARGO_HOME_ENV`, `CREDENTIALS_FILE`

## Submodules
- `resolver` — env-var + credentials-file resolution; `AuthInfo`/`TokenSource`; `mask_token`, `cargo_home_path`
- `credentials` — `credentials.toml` parsing (both strict and extended/alias-aware forms); `list_configured_registries`
- `oidc` — trusted-publishing env-var detection

## Invariants
- Tokens are opaque strings; NEVER log them.
- Whitespace-trimmed; empty tokens treated as absent (at the top-level `resolve_token` layer).
- OIDC detection: requires both `ACTIONS_ID_TOKEN_REQUEST_URL` and `ACTIONS_ID_TOKEN_REQUEST_TOKEN` to contain non-blank values; blank or whitespace-only values are treated as missing.
