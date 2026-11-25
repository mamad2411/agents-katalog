---
name: release-prep
description: Prepare a new agentsync release — validates goreleaser config, summarizes commits since the last tag against the changelog filters in .goreleaser.yaml, proposes the next semantic version, and runs a snapshot build. Does NOT tag or push — that remains a manual step requiring user confirmation.
---

# Release Prep

Goal: produce a release-readiness report and a proposed version bump for the user to approve. **Never tag, push, or invoke `goreleaser release` (non-snapshot) yourself** — those actions affect remotes and are out of scope.

## Procedure

### 1. Confirm clean state

```bash
git status --porcelain
git rev-parse --abbrev-ref HEAD
```

Abort with a clear message if there are uncommitted changes or the branch is not `main`. Releases should cut from a clean `main`.

### 2. Identify the current and previous tag

```bash
git describe --tags --abbrev=0    # latest tag, e.g. v0.4.2
git tag --sort=-v:refname | head -5
```

### 3. Summarize commits since the last tag

```bash
git log <last-tag>..HEAD --pretty=format:'%h %s'
```

Group the output by the changelog regex groups in `.goreleaser.yaml` (`Features` = `^.*feat[(\w)]*:+.*$`, `Bug fixes` = `^.*fix[(\w)]*:+.*$`, `Refactors` = `^.*refactor[(\w)]*:+.*$`, `Other` = everything not excluded by `^docs:`, `^chore:`, `^test:`, `^ci:`, `^style:`).

### 4. Propose the next version

Apply conventional-commit semver inference:

- Any `feat!:` / `BREAKING CHANGE:` → bump **major**.
- Any `feat:` (and no breaking) → bump **minor**.
- Only `fix:` / `refactor:` / `chore:` → bump **patch**.
- No commits since last tag → no release; report and stop.

State the proposed version and the rule that produced it.

### 5. Validate the goreleaser config

```bash
make release-check        # runs `goreleaser check`
```

Surface any errors verbatim.

### 6. Build a snapshot

```bash
make release-snapshot     # goreleaser release --snapshot --clean --skip=publish
```

This validates that the build pipeline (`builds`, `archives`, `homebrew_casks` rendering) succeeds locally without publishing. Then list `dist/` and confirm the expected per-OS/per-arch archives are present:

```bash
ls dist/
```

### 7. Report

```
# Release prep: <proposed-version>

## Branch: main (clean)
## Last tag: <vX.Y.Z>
## Commits since: N

### Features
- <hash> <subject>

### Bug fixes
- <hash> <subject>

### Refactors
- <hash> <subject>

### Other
- <hash> <subject>

## Proposed version: <vX.Y.Z+1>
## Bump rule: <major | minor | patch> — <one-line justification>

## goreleaser check: <pass/fail>
## snapshot build: <pass/fail>
## dist artifacts: <count> archives
```

End with the exact commands the user can run to actually cut the release — do not run them:

```
git tag <vX.Y.Z+1>
git push origin <vX.Y.Z+1>
```

The Homebrew tap publish path requires the `HOMEBREW_TAP_KEY` env var (see `.goreleaser.yaml` and `a7e56d3`); flag this if the env var is unset locally so the user knows the publish step will need it in CI.
