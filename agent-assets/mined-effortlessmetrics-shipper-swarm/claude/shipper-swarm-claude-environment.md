# Module: `crate::runtime::environment`

**Layer:** runtime (layer 2)
**Single responsibility:** OS/arch/CI environment fingerprint capture for receipt evidence.
**Was:** standalone crate `shipper-environment` + in-tree shim wrapper (absorbed; dual-impl collapse was PR #53).

## Public-to-crate API

- `CiEnvironment` — enum of detected CI providers.
- `EnvironmentInfo` — full captured environment (ci, os, arch, rust/cargo versions, env vars, timestamp).
- `detect_environment()` — returns the current `CiEnvironment`.
- `is_ci()` — returns true if any CI provider is detected.
- `collect_environment_fingerprint()` — structured `EnvironmentFingerprint` for receipts (uses the deduped PR #53 shim logic with graceful fallback).
- `get_environment_fingerprint()` — short pipe-separated fingerprint string.
- `get_rust_version()`, `get_cargo_version()` — raw `rustc --version` / `cargo --version` capture.
- `get_ci_branch()`, `get_ci_commit_sha()`, `is_pull_request()` — CI-specific helpers.

## Invariants

- CI detection is by env vars with fixed priority order: `GITHUB_ACTIONS` > `GITLAB_CI` > `CIRCLECI` > `TRAVIS` > `TF_BUILD` > `JENKINS_URL` > `BITBUCKET_BUILD_NUMBER` > `Local`.
- `normalize_tool_version` returns the second whitespace-separated token (strips `rustc ` / `cargo ` prefixes).
- `collect_environment_fingerprint` never panics: falls back to minimal info (`"unknown"` versions) if `EnvironmentInfo::collect` fails, and uses `env::consts::OS`/`ARCH` for the os/arch fields.
- `collect_env_vars` only captures a fixed allowlist of known CI variables — never arbitrary env vars.

## Layer discipline

Layer 2 (runtime): may import `crate::types`, external pure-data crates. Must not import from `crate::engine`, `crate::plan`, `crate::state`. All items `pub(crate)`.
