---
name: dep-sync
description: |
  Actively fix dependency, build, and deploy drift for CG-Agent-Harness by
  comparing the current branch's Cargo manifests/locks, toolchain pin, deny
  policy, and CI/release/packaging config against the latest origin/main and applying the needed updates, then
  re-verifying. Use when a branch has fallen behind main's dependency/toolchain
  state, after a security advisory lands on main, or whenever asked to "sync
  deps" / "fix dependency drift".
compatibility: |
  Requires: cargo, rustup, cargo-deny 0.20+ (0.18 rejects deny.toml), git; node >=20 and npm only for the browser lock
  Context: Independent backend (root, Rust 1.89) and desktop (desktop/, Rust
  1.90, macOS-only) Rust crates, each with its own Cargo.lock and deny policy,
  plus the npm lock of the /browse Playwright sidecar (browser/)
---

# dep-sync — fix dependency/build/deploy drift against origin

This skill WRITES fixes. For a report only, run steps 1, 2 and 4 with no edits
and record commands, exit codes and advisory freshness.

## 1. Establish the comparison base

```bash
git fetch origin main
BASE=origin/main
git diff --stat HEAD..."$BASE" -- Cargo.toml Cargo.lock rust-toolchain.toml \
  deny.toml .cargo/config.toml desktop/Cargo.toml desktop/Cargo.lock \
  desktop/rust-toolchain.toml desktop/deny.toml browser/package.json \
  browser/package-lock.json tests/fixtures/cargo-sandbox \
  .github/workflows/ .github/dependabot.yml scripts/package-desktop.sh
```

Always compare `origin/main` (a branch's own upstream makes the diff falsely
empty); `HEAD...$BASE` is what this branch is missing. An empty diff means
current: say so and stop; never manufacture an update. If behind, merge the
base first (never rebase someone else's branch).

## 2. Identify what origin/main changed that this branch hasn't picked up

For each file in the diff, extract the semantic change, not just the text:

- `Cargo.toml` / `desktop/Cargo.toml` — added/removed/bumped crates, features
- `Cargo.lock` / `desktop/Cargo.lock` — resolved versions (regenerate, never
  hand-edit)
- `rust-toolchain.toml` / `desktop/rust-toolchain.toml` — MSRV/channel (backend
  1.89 and desktop 1.90 are independent)
- `deny.toml` / `desktop/deny.toml` — ignores, license allowlist, bans (same
  telemetry-SDK bans in both; desktop evaluates Apple targets only, ignores empty)
- `browser/package.json` + `package-lock.json` — the sidecar's exact Playwright
  pin, also named in `docs/Browser-Use.md` and `NPM_VERIFIED_PINS` in
  `check_otel.py`; move all together and refresh the sidecar row's `reviewed`
  after re-reading the changelog. Oracle check T6 warns on disagreement and
  fails `telemetry-contract.yml`; `rg` the old version for any other copy.
  Chrome is not a repo dependency: the sidecar drives the runner's
  installed Google Chrome (`channel: "chrome"`; `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`
  is contractual). Never add `playwright install` or a browser download; Chrome
  moves with the runner image (`ubuntu-26.04`), not a repo file
- `tests/fixtures/cargo-sandbox` — a third lock CI checks with the root policy
- `.github/workflows/*.yml` (list the directory; the dependency-bearing ones
  are `ci.yml`, `clippy-sarif.yml`, `dependency-advisories.yml`, `desktop.yml`,
  `desktop-check.yml`, `bundle.yml`, `release.yml`, `install-macos.yml`,
  `netconnect.yml`, `live-ollama.yml`; all but `install-macos.yml` and
  `dependency-advisories.yml` hard-code Rust 1.89, desktop jobs also 1.90) —
  toolchain versions, runner labels, cached paths, new required jobs
- `.github/dependabot.yml` — ecosystems (Actions, cargo for both crates, npm
  for `browser/`) and the 7-day cooldown
- `scripts/package-desktop.sh`, `docs/RELEASING.md`, `docs/DESKTOP.md` —
  packaging order or signing steps that reference dependency/toolchain state

## 3. Apply the sync

Never let one crate's toolchain change leak into the other (`desktop/` is not
a workspace member).
`.cargo/config.toml` sets `resolver.incompatible-rust-versions = "fallback"`,
so a plain `cargo update` stays inside each MSRV.

```bash
# Backend (rustup's cargo reads rust-toolchain.toml and installs 1.89)
cargo fetch --locked
cargo update --dry-run --locked --verbose
# after reviewing the dry run against origin/main's diff, one package at a
# time (no --locked: a real update would fail on it):
cargo update -p <crate>
cargo deny --all-features check
# Seatbelt fixture lock, root policy; ci.yml skips licenses here:
cargo deny --manifest-path tests/fixtures/cargo-sandbox/Cargo.toml \
  --config deny.toml check advisories bans sources

# Desktop (resolves anywhere; compiles only on macOS)
cd desktop
cargo fetch --locked
cargo update --dry-run --locked --verbose
cargo update -p <crate>
cargo deny --all-features check
cd ..

# Browser sidecar lock (installs nothing)
(cd browser && npm audit --package-lock-only)
(cd browser && npm view playwright dist-tags.latest)
```

A Playwright bump is one exact pin (`npm install --save-exact --ignore-scripts
playwright@X`), never a range. Its real check is CI's `browser-guards` job
(installed Chrome, non-root, sandbox on), which refuses root: a root cloud
session cannot reproduce it, so say so; `npm audit` alone is not a pass.

Respect `docs/DEPENDENCIES.md#retained-constraints`: exact pins (`rmcp`,
`keyring-core`, desktop `tauri`), MSRV holds (`ordered-float`), listed
incompatible major lines, dated waivers. A pin origin/main still carries is not
drift; sync only what it moved. A compatible release under Dependabot's 7-day
cooldown is not drift unless it fixes an advisory against a locked crate. One
`cargo update -p` per package; check no unrelated edge re-resolved. Never add a
`cargo deny` exception to silence a finding the sync introduced; fix the version.

For CI/build/deploy YAML, copy origin/main's exact toolchain strings and job
structure; do not paraphrase.

## 4. Re-verify

Inspect new Cargo features and each new `unsafe` block's safety argument.

```bash
cargo build --all-targets --locked
cargo fmt --all -- --check
cargo clippy --all-targets --all-features -- -D warnings
# the three cargo deny commands from step 3
# Targeted only; CI runs the suite:
GROK_API_KEY="" ANTHROPIC_API_KEY="" DEEPAGENT_API_KEY="" cargo test --test <target>
# macOS only; on Linux the desktop compile is CI's `desktop compile (macos-latest)`:
cd desktop && cargo build --all-targets --locked && cd ..
```

A network dependency that moved (reqwest, rmcp, rustls, hyper, tauri, Playwright, a
new direct dependency) also drifts the telemetry oracle (`telemetry-contract.yml`): ask
the operator to run `/cgagentharness-otel-hardening` (operator-only).

Never pipe a pass/fail command into grep or suppress its exit status. A missing
`cargo-deny` is a missing required check, not a pass. Never change global rustup
overrides or git identity to make verification succeed.

## 5. Report

List: base ref, exact diffs applied per file, commands with exit codes, and each
`docs/DEPENDENCIES.md` pin deliberately left alone and why. Update its dated
"Last synchronization" section. A stale version number there: fix a one-line
change now, or ask the operator for `/doc-sync` (manual-only,
`disable-model-invocation: true`; never self-load it).

Skill selection does not authorize push/merge: follow the repo's PR conventions
(draft, `[infra]` or `[security]` prefix, `scripts/check-pr-template.sh`, `AGENTS.md`).
