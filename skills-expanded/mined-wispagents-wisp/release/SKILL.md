---
name: release
description: Use when cutting a wisp v2 release - bumping the version of the published package and letting release.yml publish npm, the desktop app, the GitHub release and the Homebrew tap.
---

# Release

v2 ships on npm as `wisp-agents` only (ADR-0094): the launcher (a dependency-free script with the web build in
`web/`) and, per target, the Rust `wisp` binary as a version of `wisp-agents` itself, `<version>-<os>-<arch>` under
the dist-tag `platform-<os>-<arch>` (`npm/README.md`). The launcher installs each through an npm alias
(`wisp-agents-<os>-<arch>`: `npm:wisp-agents@<version>-<os>-<arch>`), pinned to its own version, so they all publish
together, and wisp-agents' one trusted publisher covers every tarball: nothing is ever published by hand.

1. Releasing is merging a PR that bumps the version in **both** `Cargo.toml` (`[workspace.package] version`: what
   `wisp --version` prints; then `cargo update --workspace` so `Cargo.lock` follows; the spikes keep their own locks: `for s in events server-budgets sync-bench-rs; do cargo metadata --format-version 1 --manifest-path spikes/$s/Cargo.toml >/dev/null; done`, or CI's suite fails on `main` with "spikes/…/Cargo.lock is stale") and
   `npm/wisp-agents/package.json` (`version` and every `npm:wisp-agents@<version>-<os>-<arch>` pin in `optionalDependencies`).
   `node npm/scripts/release.mjs check` says whether they (and `Cargo.lock`) agree (release.yml's plan job runs
   it first and fails with the file to fix). Every built-in plugin's manifest carries the same version (Settings →
   Plugins shows it): `node npm/scripts/release.mjs set-plugins <version>` sets all of `plugins/*/host/wisp-plugin.json`,
   and `check` (and `crates/wisp/tests/builtin_versions.rs`) refuse a mismatch. Built-ins require each other with
   `^1.0.0-0`, which takes every 1.0.0 pre-release and every 1.x; a pre-release of another x.y.z (`1.1.0-beta.1`)
   needs those ranges moved to `^1.1.0-0` in the same PR (the test says which). Also bump the strings that show it: `README.md`, `docs/index.html`,
   `docs/install.sh`, `scripts/guides.mjs`.
2. Move CHANGELOG's *Unreleased* into `## [x.y.z] - YYYY-MM-DD`: `scripts/release-notes.mjs` drafts the GitHub
   release from that section (the plan job fails without it).
3. `.agents/bin/monoflow verify --all` and `npm run check` pass before the PR is opened.
4. After the merge (a push that changes `npm/wisp-agents/package.json`'s version; a `Cargo.toml` dependency edit
   releases nothing), `release.yml` sees a version npm doesn't have and:
   - **binaries**: `cargo build --release --locked -p wisp` for every target in `npm/wisp-agents/lib/resolve.js`
     `TARGETS` (Mac and Windows natively, Linux static musl through cargo-zigbuild; runners in
     `npm/scripts/release.mjs` `buildMatrix`);
   - **packages**: `npm run build` (the web bundle), `npm/scripts/build.mjs` per target, the launcher's tests
     (`node --test npm/test/`), `npm pack`, then the packed linux-x64 tarballs run `wisp --version` and
     `wisp serve` (the web UI is served from the launcher's `web/` through `WISP_WEB_DIR`);
   - **desktop**, **release** (the draft, with the desktop downloads and each binary as
     `wisp-bin-<os>-<arch>.tar.gz` for the machines plugin's installer), **npm** (those exact tarballs, `--provenance`: every binary version
     first under `platform-<os>-<arch>`, the launcher last under its channel's tag, each version npm already has skipped), **publish** (the release goes
     public), **homebrew** (the tap points at the `wisp-agents` npm tarball; npm brings the platform package).
   A run that stopped half way is finished by re-running it (Actions → release → Run workflow).
5. `x.y.z-alpha.N` (`1.0.0-alpha.1`) is the public channel while wisp is in alpha: it ships like a stable release
   (npm `latest`, the GitHub release marked Latest, Homebrew formula and cask, the updater's default channel) and
   npm's `alpha` dist-tag also names it (the trusted publisher needs "Allow npm dist-tag" on npmjs.com; without it
   the npm job warns). Any other `-` (`1.0.0-beta.1`, `-rc.1`) is a beta: npm `next`, a prerelease, no Homebrew.
   The rule is `npm/scripts/release.mjs` `releaseKind`. Nightlies are
   `<next patch>-nightly.<date>.<time>` on npm `nightly`, stamped into `Cargo.toml` and every npm package.
6. Try the whole build on a branch without publishing: `gh workflow run release --ref <branch> -f dry_run=true`
   (the tested tarballs are the run's `npm-packages` artifact).

npm trusted publishing (OIDC) is set up on npmjs.com for `wisp-agents`: repo WispAgents/wisp, workflow
`release.yml`, environment `npm`. Every tarball is a version of that one package (ADR-0094), so it covers them all,
a new target included: nothing is published by hand and there is no npm token.
