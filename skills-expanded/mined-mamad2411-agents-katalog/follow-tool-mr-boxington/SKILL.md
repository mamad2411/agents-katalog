---
name: follow-tool-mr-boxington
description: Set up and use mbx (mr boxington) — shared cache for Cargo builds across worktrees and CI
argument-hint: "[scope]"
related:
  - follow-tool-mise
  - follow-tool-cargo
  - follow-lang-rust
  - follow-tool-github-actions
  - resolve-errors
  - optimize
  - use-git-worktrees
  - setup-cicd
  - cleanup-artifact
  - follow-tool-nextest
---

## Goal

Set up and use mbx (Mr Boxington) as a shared compiler cache for Cargo builds — reuse compilations across projects, worktrees, and CI, with managed `target/` and a machine-wide scheduler

## Scope

For Rust projects that want to reuse build artifacts across checkouts/worktrees/CI with automatic `target/` cleanup

- Boundary: if you need to cache other compilers beyond Rust/C/C++ or distributed compilation → use `sccache`; mbx already defers to a `RUSTC_WRAPPER` pointing at another cache
- Latest: `mbx@1.18.0` (verified 2026-09-26, GitHub `jdx/mr-boxington` releases) — crate name `mbx`, mise tool name `mr-boxington`
- References: [cli](references/cli.md) 
## Execute

### 1. Install mbx

> Goal: have the `mbx` binary ready with the existing Rust toolchain

1. Check a Rust toolchain exists first (`cargo --version`) — mbx wraps the active Cargo/rustc; it doesn't install Rust itself (except via the mise tool `rust`)
2. Recommended via mise (requires mise ≥2026.9.2): `mise use --global --tool-option mr_boxington=true rust mr-boxington` — gets Rust + mbx + Cargo wrapping without `mbx setup`; drop `--global` for project-only
3. Older mise (2026.8.16–2026.9.1): `mise use --global --postinstall "mbx setup --yes" mr-boxington`
4. Alternatives: `cargo install mbx --locked` or release archives from GitHub Releases (verify `SHA256SUMS` first) — platforms: Linux x86-64/ARM64 (gnu+musl), macOS ARM64, Windows x86-64/ARM64
5. If the project has no mise → do `/follow-tool-mise` first
6. Confirm with `mbx --version` and `mbx doctor`

### 2. Enable Cargo Wrapping

> Goal: plain `cargo build`/`cargo test` flow through mbx

1. mise native (≥2026.9.2): the tool option `mr_boxington = true` in the `[tools] rust` entry enables wrapping automatically — use `mise exec -- cargo build`, `mise run` tasks, or a shell with mise activation/shims
2. Share with the project by committing to `mise.toml`:
   ```toml
   [tools]
   rust = { version = "stable", mr_boxington = true }
   mr-boxington = "latest"
   ```
3. Standalone (no mise, or when rust-analyzer integration is needed): `mbx setup` installs a stable Cargo shim — scope: `--global`, `--local`, or `--yes` to accept the recommendation; check with `mbx setup --status`
4. Verify `cargo` resolves to the wrapper/shim: `where.exe cargo` (Windows) or `command -v cargo` (Unix)
5. Desktop apps/agents that don't inherit PATH → use `mise exec -- cargo build` or prepend the shim dir printed by `mbx setup`
6. Remove wrapping: drop `mr_boxington` from the Rust tool entry + `mise reshim`; if `mbx setup` was used → `mbx setup --uninstall` per scope

### 3. Run Builds

> Goal: build/test/clippy through mbx with the same Cargo args

1. Any `mbx <cargo-subcommand>` works: `mbx build`, `mbx test --workspace --all-features`, `mbx clippy --workspace --all-targets -- -D warnings`
2. Pick toolchains rustup-style: `mbx +stable check --workspace`
3. Cargo aliases and installed subcommands still work — reuse the same toolchain/features/profile across builds to reuse the same cache
4. The first build fills the store — no hits yet; mbx creates a managed target and leaves a `target` symlink in the workspace (an existing `target/` is moved into the managed root with its outputs)

### 4. Verify Cache Reuse

> Goal: confirm compilations are actually restored

1. Run `mbx doctor` — checks the Cargo/rustc pair, wrapping, and store health (mise native: doctor may warn about a missing standalone shim even when wrapping works — verify with a real build)
2. Read the post-build summary: `hits` = restored, `misses` = compiled fresh then filled the cache, `bypassed` = didn't go through the shared cache
3. Rebuilding into an up-to-date `target/` doesn't count as a hit — test reuse with a fresh target dir or a new worktree on the same command
4. No hits → `mbx explain --last` for the reason per action; watch live with `mbx tui` and summarize with `mbx stats`

### 5. Manage Targets And Cache

> Goal: `target/` is managed and the store doesn't bloat

1. Managed targets are on by default: `target -> <cache root>/targets/v1/<checkout digest>` — mbx adds the link to `.git/info/exclude` itself
2. `mbx adopt` moves an existing `target/` into management without deleting: `mbx adopt`, `mbx adopt ~/src/project`, `mbx adopt --recursive --dry-run ~/src`
3. Collection runs automatically after builds (at most hourly): removes targets of missing checkouts, unused >`target.max_age` (30d), and LRU beyond `target.max_size` (10% of disk)
4. Inspect the store: `mbx cache stats`, `mbx cache projects`, `mbx cache largest`, `mbx cache dir`; preview cleanup with `mbx gc --dry-run` before `mbx gc`
5. Explicit `CARGO_TARGET_DIR`/`--target-dir`/`build.target-dir` → mbx leaves that target alone

### 6. Schedule Parallel Builds

> Goal: multiple builds/agents share one CPU+memory budget

1. The scheduler is on by default — pool of `scheduler.cpus` (default = logical CPUs) − `scheduler.reserve_cpus`, memory default 85% of RAM; cache hits don't wait for a permit
2. Parallel Cargo commands need a separate `CARGO_TARGET_DIR` per command (the Cargo lock serializes on a shared target) — mbx dedupes identical in-flight work itself
3. Include test binaries in the pool: `scheduler.tests = true` or `MBX_SCHEDULER_TESTS=1 mbx test --workspace` — useful when several agents/test suites run at once
4. Low priority for editor/background: `scheduler.priority = "low"`; pressure control pauses admission when memory is tight (`scheduler.pressure`, default on)

### 7. Configure Settings

> Goal: tune behavior with correctly scoped config

1. Precedence: `MBX_*` env → `.mbx.toml` at the workspace root (workspace settings only) → `mbx/config.toml` in the platform config dir (`%APPDATA%\mbx\config.toml` on Windows)
2. Unknown TOML keys are rejected — a typo errors immediately
3. Common settings: `gc.max_size`, `target.max_size`/`target.max_age`, `scheduler.reserve_cpus`, `summary = "short"|"full"|"ci"|"off"`, `savings = "quips"|"plain"|"off"`, `[linker.profiles.*]`
4. `[remote]` settings are accepted only in global config or `MBX_REMOTE_*` env — a repo `.mbx.toml` won't take them
5. See all settings details in 

### 8. Set Up CI Sharing

> Goal: CI restores cache published by trusted builds

1. GitHub Actions: use `jdx/mr-boxington-action@v1` before the build step — pushes to the default branch save entries, PRs (including forks) are restore-only; see full inputs at 
2. Remote cache server: `[remote] url`, `namespace` (required when url is set), `mode = "read-write"` + bearer token or OIDC (`id-token: write`)
3. S3-compatible (incl. R2/MinIO): `url = "s3://bucket[/prefix]"` + AWS env credentials + `s3_endpoint`/`s3_region` for non-AWS
4. Other transports: `MBX_CACHE_EXPORT_GROUP` per job → `mbx cache export --group <g> out.tar` / `mbx cache import in.tar`
5. The write policy is always enforced on the environment side — PR contexts never publish even when config is `read-write`

## Rules

### 1. Installation And Wrapping

- Prefer `mise use -g --tool-option mr_boxington=true rust mr-boxington` (mise ≥2026.9.2) per `global_rules` — don't `cargo install` when mise manages Rust
- Keep the existing Rust version pin when adding `mr_boxington = true` — edit only the tool entry, don't change the version
- `mbx setup` writes an explicit `[wrappers.cargo]` (requires mise ≥2026.8.16) — an explicit wrapper takes precedence over the Rust tool option
- Upgrade via the original install method — the stable shim follows upgrades without re-setup

### 2. Compiler Cache Interop

- If `RUSTC_WRAPPER` points at another cache (`sccache`, `kache`) → mbx forwards compilations to that cache and doesn't cache itself — pick one, don't stack
- `mbx exec` for C/C++ builds outside Cargo: `mbx exec make -j8`, `mbx exec cmake --fresh -S . -B build`
- Never delete the cache dir while a build is running — the cache can always be rebuilt, but an interrupted build cannot

### 3. Storage And Filesystem

- The working cache + target must be on local storage — mbx rejects NFS on Linux/macOS (`cache_dir`/`MBX_CACHE_DIR`, `target.root`/`MBX_TARGET_ROOT`)
- Reflinks need a CoW filesystem: APFS (macOS), btrfs/XFS (Linux), ReFS/Dev Drive (Windows) — NTFS/ext4 fall back to byte copy (the cache still works)
- Windows: the `target` symlink needs Developer Mode or a privileged process — if it can't be created, Cargo continues with a normal target
- Always preview before deleting: `mbx gc --dry-run`, `mbx adopt --dry-run`

### 4. Caching Limits

- Incremental compilations are not shared — mbx forces `CARGO_INCREMENTAL=0` and keeps learned incremental state private per checkout (`gc.incremental_max_size`)
- Build-script execution is cached per `rerun-if-changed`/`rerun-if-env-changed` — disable with `build_script_execution = false`
- Native links cache only on hosts the linker/SDK/CRT can describe (Linux, macOS, Windows MSVC/LLVM) — `cache_links`/`MBX_CACHE_LINKS=0` disables
- Built-in WASM targets (`wasm32-unknown-unknown`, `wasm32-wasip1/2`, `wasm64-unknown-unknown`, etc.) cache on every platform

### 5. Safety And Verification

- `mbx doctor` + a representative build before concluding the setup works — a binary merely installed is not proof cargo uses mbx
- A repo `.mbx.toml` holds workspace settings only — never put remote URLs, credentials, or machine paths in it
- Scope remote write credentials to trusted branches — PR jobs use a read-only role
- Hit an error → do `/resolve-errors`; see [references/cli.md](references/cli.md) for debug commands (`explain`, `cache trace`, `cache verify`)

- Use `/follow-tool-mise` for installing/managing tool versions
- Use `/follow-tool-cargo` for Cargo config and lint rules
- Use `/follow-lang-rust` for Rust project structure
- Use `/follow-tool-github-actions` for general CI workflows

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- `mbx` installed and `cargo`/`mbx` builds go through the shared cache
- `mbx doctor` passes and repeat builds across a worktree/fresh target show real cache hits
- `target/` is managed and collection reclaims disk automatically
- CI restores from cache published by the default branch (when configured)
- Parallel builds share one CPU/memory budget without overwhelming the machine
