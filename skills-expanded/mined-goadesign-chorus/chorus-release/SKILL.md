---
name: chorus-release
description: Release Chorus, including dependency updates, Goa code regeneration, C4 architecture diagram refresh via mdl, preflight race tests, semver version bumps, multi-arch release tarball builds, and publishing GitHub releases. Use when the user asks to release Chorus, prepare a Chorus release, bump the Chorus version, or run make release.
---

# Chorus Release

Use this skill only from the Chorus repository (`github.com/goadesign/chorus`). `make release`
regenerates Goa-AI MCP code and the architecture diagram, runs preflight checks, creates and pushes
the release commit and tag, builds multi-platform release archives (`darwin/amd64`, `darwin/arm64`,
`linux/amd64`, `linux/arm64`, and `checksums.txt`), publishes the GitHub release, and warms the Go
module proxy. Do not run `make release` unless the user explicitly approves that exact release.

## Release Contract

- Resolve the target version before making dependency-update or version-bump commits. Pick the
  version from the changes since the previous release tag, explain the reasoning, and get user
  confirmation before editing files or running dependency updates unless the user already specified
  the target version.
- Apply semantic versioning (`vMAJOR.MINOR.BUILD`):
  - Patch release: increment `BUILD` (fixes, dependency updates, docs, tests, or internal polish).
  - Minor release: increment `MINOR` and reset `BUILD=0` (new user-visible capability, CLI command,
    or backward-compatible MCP/Go API addition).
  - Major release: increment `MAJOR` and reset `MINOR=0`, `BUILD=0` only when explicitly requested.
- The preparation commit message must be `Prepare vX.Y.Z`.
- Keep the working tree clean between phases. Never discard local changes unless the user
  explicitly approves it.

## Version Selection

Determine the target version before changing the repository:

1. Read `MAJOR`, `MINOR`, and `BUILD` from `Makefile`.
2. Inspect the commits and merged PRs since the previous release tag (`git log <prev-tag>..HEAD`).
3. Pick the semver bump and confirm the target version `vX.Y.Z` with the user.
4. Use the exact confirmed target version for every preparation commit, tag check, and release
   command.

## Pre-Check

Before preparing the release, verify the repository state:

1. Run `git status --porcelain` and stop if there are uncommitted changes.
2. Verify the current branch is `main` (`git branch --show-current`).
3. Run `git fetch origin`.
4. Verify `git rev-list --left-right --count @{u}...HEAD` reports `0 0`. If behind, run
   `git pull --ff-only origin main`. If ahead or diverged, stop and ask.
5. Verify the target tag `vX.Y.Z` does not already exist locally or on `origin`.

## Preparation Workflow

1. **Update all Go dependencies and tools**:

   ```bash
   make depend
   ```

   This runs `go get -u -v ./...`, `go mod tidy`, and installs the latest `goa` and `mdl` CLIs.

2. **Regenerate Goa-AI MCP code and refresh the architecture diagram**:

   ```bash
   make gen
   make diagram
   ```

   - `make gen` runs `goa gen github.com/goadesign/chorus/design` to ensure `gen/` matches the
     latest `goa` and `goa-ai` generators.
   - `make diagram` runs `mdl svg` and `mdl gen` on `github.com/goadesign/chorus/diagram` so
     `diagram/Chorus Architecture.svg` and `diagram/design.json` are up-to-date.
   - If `diagram/model/model.go` or `diagram/views.go` changed since the last release, follow the
     `editing-model-diagrams` skill to visually inspect `diagram/Chorus Architecture.svg` (or refine
     layout via `mdl serve`) and confirm there are no overlapping labels or clipped text.

3. **Run lint and race-enabled release tests**:

   ```bash
   make lint test-release
   ```

   Fix any failures before continuing.

4. **Update `MAJOR`, `MINOR`, and `BUILD` in `Makefile`** for the target version `vX.Y.Z`.

5. **Commit preparation changes** (if `go.mod`, `go.sum`, `gen/`, `diagram/`, or `Makefile`
   changed):

   ```bash
   git add .
   git commit -m "Prepare vX.Y.Z"
   ```

   Do not push manually; `make release` pushes `main` together with the release commit and tag.

## Final Pre-Release Check

Before running `make release`:

1. Run `git fetch origin`.
2. Verify `git status --porcelain` is empty.
3. Verify upstream is not ahead (`git rev-list --left-right --count @{u}...HEAD` starts with `0`).
4. Reconfirm that `vX.Y.Z` is absent locally and on `origin`.

## Run And Babysit Release

1. Run `make release`.
2. Watch the command until it exits. `make release` performs these steps in order:
   - Updates `Version("X.Y.Z")` in `design/design.go` and `diagram/model/model.go`.
   - Runs `make release-preflight` (`gen`, `diagram`, `lint`, `test-release`).
   - Commits `Release vX.Y.Z` (if version strings changed) and creates tag `vX.Y.Z`.
   - Pushes `main` and `vX.Y.Z` to `origin`.
   - Builds `darwin/amd64`, `darwin/arm64`, `linux/amd64`, and `linux/arm64` release tarballs plus
     `checksums.txt` in `dist/`.
   - Creates the GitHub release `vX.Y.Z` with the binary archives attached.
   - Warms `proxy.golang.org` and `sum.golang.org` for `github.com/goadesign/chorus@vX.Y.Z`.
3. If any step fails, stop and inspect local and remote state (`git status`, local/remote tags, and
   `gh release view vX.Y.Z`) before rerunning anything. Never delete a public tag or force-push
   without explicit user approval.

## GitHub Release Notes

After `make release` succeeds, polish the GitHub release notes for `vX.Y.Z`:

1. Gather the commit and PR list from the previous tag to `vX.Y.Z`, and identify every human
   contributor.
2. Write clear, standalone plain-English release notes for a developer who does not know Chorus
   internals:
   - Start with a concise summary of why the release matters.
   - Use sections (`Highlights`, `Fixes`, `Dependencies`, `Contributors`) only when helpful.
   - Lead with user payoff before implementation details, and include one-line install instructions:
     `curl -fsSL https://raw.githubusercontent.com/goadesign/chorus/main/scripts/install.sh | sh`.
   - Never mention AI or agent authoring tools in commits or release notes.
3. Update the GitHub release notes with `gh release edit vX.Y.Z --notes-file <file>`.
