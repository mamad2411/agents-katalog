---
name: release
description: Cut a tagged release of the splitfire-agent crate. Covers the version-bump checklist, the gate (fmt/clippy/test), fast-forwarding main, the annotated tag that fires the cross-platform release and crates.io workflows, and verifying the published GitHub release and crate. Use whenever the user asks to release, cut, tag, or publish a new splitfire-agent version.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
user-invocable: true
---

# Release

How to cut a `splitfire-agent` release. Releases are driven by git tags. Pushing a
`v*` tag fires two workflows:

- `.github/workflows/release.yml` — builds the binary on five targets
  (darwin-arm64/x64, linux-x64/arm64, windows-x64) and publishes a GitHub release
  with auto-generated notes and the archives attached.
- `.github/workflows/release-crates.yml` — runs `cargo publish --locked` to push
  the crate to crates.io, authenticated by **trusted publishing**: a GitHub OIDC
  token is exchanged for a short-lived crates.io token. There is no
  `CARGO_REGISTRY_TOKEN` secret to store or rotate.

Branch model: work lands on `development` (via PRs); `main` is the release branch;
every tag points at a commit that is on `main`. Previous tags were plain annotated
(not GPG-signed) tags authored by the maintainer, message `Release vX.Y.Z`.

---

## 0. One-time setup: the trusted publisher

Trusted publishing needs a publisher registered on crates.io **before** the first
tagged run. The crate must already be on crates.io (a first-ever publish still
needs a manual `cargo login` + `cargo publish`), and you must be a crate owner.
Then: crate page → **Settings → Trusted Publishing → Add → GitHub**:

- Repository owner: `SplitFireAI`
- Repository name: `splitfire-agent`
- Workflow filename: `release-crates.yml` (the bare filename, not a path)
- Environment: leave blank unless the job also declares `environment:`

The workflow filename is part of the trust claim, so renaming the workflow breaks
publishing until the crates.io config is updated to match — keep the two in sync.

---

## 1. Confirm the version is bumped

The version bump often already landed with the feature PR — check before assuming
you need a bump commit. These three must agree and must be the version you're
releasing:

- `Cargo.toml` (`version = "X.Y.Z"`)
- `Cargo.lock` (the `splitfire-agent` package entry)
- `registry/agent.json` (`"version": "X.Y.Z"`)

```sh
grep -m1 '^version' Cargo.toml
grep -A2 '^name = "splitfire-agent"' Cargo.lock | grep version
grep '"version"' registry/agent.json
```

If a bump is needed, edit all three, run `cargo build` to refresh `Cargo.lock`, and
commit on `development` (or the release branch) before continuing. `registry/` is the
ACP registry submission; keeping its `version` in sync with `Cargo.toml` is part of
the release, per AGENTS.md.

## 2. Run the gate

CI runs exactly these three; run them locally and get them green before tagging. Use
`cargo` directly — this is a Rust crate, the global `rv` rule is Ruby-only.

```sh
cargo fmt -- --check
cargo clippy --locked --all-targets -- -D warnings
cargo test --locked
```

## 3. Get the release commit onto main

`main` must fast-forward to the commit you're releasing (no merge commit, matching
history). Verify there is nothing on `main` that isn't on your source branch:

```sh
git log --oneline main..origin/main        # expect empty (main not ahead)
git log --oneline origin/main..development  # the commits you're about to release
```

Fast-forward `main` to the release commit (works without checking it out), then push:

```sh
git branch -f main development
git push origin main
```

## 4. Tag and push

Confirm your git identity and gh account are the maintainer's before tagging — the
`git-commit-signing` skill governs identity selection. Match the previous tag's
style: plain annotated, message `Release vX.Y.Z`. Pushing the tag is what fires the
release workflow, so push it last.

```sh
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

## 5. Verify the published release

The workflow takes ~8-9 minutes (five-target matrix). Watch it, then confirm all
five assets are attached:

```sh
gh run list --workflow=release.yml --limit 1
gh run view <run-id> --json status,conclusion,jobs \
  --jq '{status,conclusion,jobs:[.jobs[]|{name,conclusion}]}'
gh release view vX.Y.Z
```

A green release has five assets:
`splitfire-agent-{darwin-arm64,darwin-x64,linux-arm64,linux-x64}.tar.gz` and
`splitfire-agent-windows-x64.zip`.

Also confirm the crate published:

```sh
gh run list --workflow=release-crates.yml --limit 1
curl -s https://crates.io/api/v1/crates/splitfire-agent | python3 -Ic \
  'import sys,json;print(json.load(sys.stdin)["crate"]["max_version"])'
```

---

## Notes

- A release is outward-facing and hard to reverse (public binaries, cached/indexed).
  The user asking to "release vX.Y.Z" authorizes it; still report faithfully if a
  gate step fails rather than tagging anyway.
- The GitHub release is created by `github-actions[bot]`, not the tagger. That's
  expected — the workflow uses `GITHUB_TOKEN`.
- Release notes are auto-generated from merged PRs since the previous tag
  (`--generate-notes`). There is no hand-written CHANGELOG file in this repo.
- crates.io is immutable and append-only: a version can be published exactly once,
  then only *yanked* (hidden from new resolves, existing lockfiles keep working) —
  never replaced or deleted. So the tag's `Cargo.toml` version must not already be on
  crates.io; any re-release needs a fresh version bump. The `ed-*` dependencies are
  already on crates.io, so no dependency needs publishing first. To publish manually
  instead of via CI: `cargo login` once (token from crates.io/settings/tokens), then
  `cargo publish --locked` from the tagged commit.
- `crates-io-auth-action` is pinned to `v1.0.5` deliberately: the action repo has
  no moving `v1` tag (only `v1.0.x`), so the `@v1` shown in the crates.io docs
  example fails to resolve. Bump the pin when a newer release lands.
- If a platform build fails after the tag is pushed, fix the cause and re-run the
  failed jobs (`gh run rerun <run-id> --failed`); the release-create step tolerates
  an already-existing release and `--clobber`s assets, so re-runs are safe.
