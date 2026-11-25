---
name: release-sidecar
description: Release new versions of sidecar. Covers version tagging with semver, td dependency updates, go.mod validation, CHANGELOG updates, GoReleaser automation, Homebrew tap updates, and verification steps. Use when preparing or executing a release.
disable-model-invocation: true
---

# Releasing a New Version

Operator contract: **`docs/guides/active/releasing.md`**. Enforcement lives in `scripts/` and
`BUMP=minor make release` (or `RELEASE_VERSION=vX.Y.Z make release` for an explicit
version). Prefer the one-shot command over replaying this checklist by hand.

## Prerequisites

- Go matching `go.mod`
- Clean working tree; `main` identical to live `origin/main`
- Tests and **Go CI** green on the commit you will tag (tests *and* lint) —
  `check-release-state.sh` now checks this itself via `gh run list
  --workflow=go-ci.yml` and fails closed if it's red/running/missing, so you
  don't have to remember to look
- GitHub CLI authenticated with push access to `marcus/homebrew-tap`
- No `replace` directives in `go.mod`
- `HOMEBREW_TAP_TOKEN` secret present in the GitHub repo (CI tap job)

**Beware of go.work**: always use `GOWORK=off` when updating dependencies and
when validating install paths.

Local lint must match CI's golangci-lint **v2.12.2**, or trust CI:

```bash
gh run list --workflow=go-ci.yml --limit=1
```

## Prepare (sidecar-specific)

### 1. Version

```bash
git tag -l 'v*' | sort -V | tail -1
```

SemVer: major / minor / patch as usual.

### 2. Sibling dependencies (td, tasks)

```bash
make sync-deps   # pins every github.com/marcus/* requirement to its latest tag
```

`check-release-state.sh` enforces this and refuses to tag when one is behind.
`go.work` resolves those imports to the local checkouts, so drift is invisible
locally — both the gate and `sync-deps` use `GOWORK=off`. If a sibling jumped
several minors, decide deliberately (pin for a focused release vs take latest
and note it under Dependencies) and smoke its tab in the app.

### 3. CHANGELOG

```markdown
## [Unreleased]

### Features
- …

### Bug Fixes
- …

### Dependencies
- …
```

Commit the changelog (and any dependency bump) on `main`, then push so
`HEAD == origin/main`. Leave the heading as `## [Unreleased]` — `make release`
stamps it to `## [vX.Y.Z] - YYYY-MM-DD` for you.

## Publish

```bash
# Dry-run (optional but recommended for tooling changes)
make release-snapshot
./scripts/verify-release-archives.sh dist
./scripts/test-release-guards.sh dist
./scripts/test-release-publication.sh
make release-dry-run BUMP=minor   # prints the derived version + plan, no mutation

# Cut the release: derive the version, stamp the changelog, commit, push,
# then the fail-closed preflight → tag → CI → formula verify/publish
BUMP=minor make release
```

The version is stated exactly once — via `BUMP` derived from the latest tag, or
by setting `RELEASE_VERSION=vX.Y.Z` yourself (also works if you stamped the
CHANGELOG heading by hand). `scripts/release.sh` refuses an empty `[Unreleased]`
section, a tree dirty beyond `CHANGELOG.md`, a tag that already exists, and a
`RELEASE_VERSION` that contradicts an already-stamped heading, before handing off
to `scripts/publish-release.sh`. What it enforces and does end to end is
documented in `docs/guides/active/releasing.md`.

Resume only the tap step if the tag/release already exists:

```bash
RELEASE_VERSION=vX.Y.Z make release-tap
```

### CI jobs (on tag push)

1. **`verify`** — tag points at live `main`, tests, snapshot archives, release guards
2. **`release`** — GoReleaser publishes GitHub release + binaries
3. **`update-homebrew-tap`** — renders `packaging/homebrew/sidecar.rb.tmpl` and
   pushes `Formula/sidecar.rb` with downgrade/idempotency/race guards

td/nightshift formulas are **not** auto-bumped; edit them by hand when co-releasing.

## Verify

```bash
gh run list --workflow=release.yml --limit=1
gh release view vX.Y.Z --json assets -q '.assets[].name'

GOBIN=$(mktemp -d) GOWORK=off go install github.com/marcus/sidecar/cmd/sidecar@vX.Y.Z
"$GOBIN/sidecar" --version
```

`go install @vX.Y.Z` can 500 from the checksum DB for a minute or two after the
tag — wait and retry. Prefer a throwaway `GOBIN` so verification does not
clobber a dev machine's `sidecar`.

## Dev machine after release

```bash
# Return to the canonical main development build:
make install-local

# Or keep the released Homebrew build active:
make use-homebrew

# In either case, prove the managed link and both login-shell modes:
make install-status
```

## Recovery

Prefer a new patch release. Keep tags. Resume tap with `make release-tap`.
See `docs/guides/active/releasing.md`.

## Checklist

- [ ] Go CI green (tests + lint) on the commit to tag — enforced automatically by `check-release-state.sh`
- [ ] Working tree clean; `main` == `origin/main`
- [ ] td bump considered; td tab smoke if td moved
- [ ] No `replace` in go.mod; `GOWORK=off` build works
- [ ] Agent integration assets: if any bundled asset's bytes changed, its version constant, `internal/agentlifecycle/capabilities.json`, and the golden in `internal/agentintegration/asset_golden_test.go` all moved with it (the golden test fails if they did not)
- [ ] CHANGELOG bullets under `## [Unreleased]`
- [ ] `BUMP=minor make release` (or `RELEASE_VERSION=vX.Y.Z make release`) succeeded
- [ ] Release assets present; formula URL/sha match (automatic)
- [ ] `go install` verified into throwaway `GOBIN`
- [ ] `make install-status` proves the dev machine is on the intended binary
