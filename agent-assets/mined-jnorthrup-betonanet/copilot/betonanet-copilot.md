

<!-- .github/copilot-instructions.md - concise guide for AI coding agents -->

# Copilot orientation: literbike (short)

This short guide gives the essential, repo-specific context an automated coding agent needs to be productive in the literbike workspace.

Core facts
- Crate name: `literbike` (see `Cargo.toml`). Primary binary lives at `src/bin/litebike.rs` and uses argv0-dispatch to emulate `ifconfig`, `ip`, `route`, `netstat`.
- Default unified proxy port: 8888 (env var: `LITEBIKE_BIND_PORT`). Tests and CI rely on this; changing it requires test updates.

Quick read path (first 10 minutes)
- `src/bin/litebike.rs` — argv0 dispatch, `WAM_DISPATCH_TABLE`, pattern for adding subcommands (wrapper signature: `fn(&[String])`).
- `src/config.rs` — env-driven configuration. Use `Config::from_env()` and `cfg.apply_env_side_effects()` when tests must emulate runtime.
- `src/syscall_net.rs` and `src/syscall_net/` — platform syscall, netlink, ioctl helpers (common source of platform-specific bugs).
- `src/lib.rs` — crate exports and the smoke test.
- `tests/README.md` — canonical test matrix and CI commands.

High-value conventions and examples
- Subcommands: add a `WAM_DISPATCH_TABLE` entry + a thin wrapper `fn(&[String])` that calls the implementation. Keep wrappers stable (no signature changes).
- Config: prefer env-driven flags. Example in tests:
	let cfg = literbike::config::Config::from_env();
	cfg.apply_env_side_effects();
- Re-exports: tests sometimes expect crate-level re-exports (e.g. `protocol_registry` or detector traits). Adding small shim modules or `pub use` re-exports is acceptable and low-risk.

Build / test / CI (concrete)
- Build workspace: `cargo build --workspace`
- Run full tests: `cargo test --workspace`
- Feature-matrix examples: `cargo test --features full`, `cargo test --no-default-features`
- Benchmarks: `cargo bench` (see `tests/benchmarks/`)
- CI: tests depend on feature matrix and the unified port; check `tests/README.md` and `.github/workflows` if present.

Safe, small edits an agent can make
- Fix crate-name typos (`litebike` → `literbike`) and small wrapper-arg passing bugs.
- Add focused shims/re-exports to satisfy tests (minimal, typed stubs) instead of large refactors.
- Add or update env flags in `src/config.rs` by updating both `from_env()` and `apply_env_side_effects()`.

Integration points and gotchas
- Network code uses raw syscalls and netlink/ioctl; platform differences are guarded with `cfg(target_os)`.
- Tests may bind to network ports; prefer binding to port 0 in tests and read back the assigned port to avoid collisions.
- External tool fallbacks (ss/netstat/busybox/networksetup) are referenced — be conservative changing those paths.

Where to ask for help
- For ambiguous design changes add a one-line `TODO: MAINTAINER: ...` comment in the changed file and open a small PR.

If you'd like, I can expand this guide with: (a) a minimal onboarding checklist, (b) targeted examples for adding a subcommand, or (c) a short test-writing template. Tell me which and I will iterate.

