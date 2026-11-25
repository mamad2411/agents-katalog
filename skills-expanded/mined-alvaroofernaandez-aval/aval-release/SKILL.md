---
name: aval-release
description: "Use when cutting, checking or publishing an aval release: versioning, the CHANGELOG, an rc or beta, promote, tags, GoReleaser. An ordered checklist that stops at the first failure; publishing only with explicit authorization."
---

## Activation contract

Load before `aval release` or any tag, version or CHANGELOG work. Maintainer reference: `docs/releasing.md`. Where it disagrees with a global skill, this one wins (`AGENTS.md`).

## Hard rules

- **Never push unasked.** `aval release rc|beta|patch|minor|major|promote` creates an annotated tag and runs `git push origin <tag>`. That is a remote, public action: run a cutting command only after the owner's explicit authorization for that exact version. Without it, stop at `--dry-run`.
- The `release` environment approval in GitHub is the owner's alone. Never ask for or simulate it. Only the first stable release of a breaking line (a new minor before 1.0, a new major) waits for it; prereleases, patches and minors after 1.0 publish from `release-patch`, which needs no approval (owner decisions, 2026-11-23).
- Prerelease (`-rc.N`, `-beta.N`) or stable is the owner's decision.
- Never print or commit tokens (`NPM_TOKEN`, `GH_TOKEN`).
- Conventional Commits, no AI attribution: the release notes are generated from commit subjects.

## Checklist (in order; stop at the first failure and report it)

1. **Clean `main`.** `git status` clean, on `main`, up to date with `origin/main`. `aval release` refuses otherwise.
2. **Notes and CHANGELOG.** Write both notes first, following the `aval-release-notes` skill: `docs/releases/vX.Y.Z.md` (English) and `docs/releases/vX.Y.Z.es.md` (Spanish; an rc uses the base version's files), every number measured. `CHANGELOG.md` has its `## vX.Y.Z-rc.N (date)` section with a short summary and a line linking both notes (`tests/release_notes_test.go` and `tests/hub_docs_test.go` pin this). Past entries are not hand-edited. Read the grouped notes `aval release status` prints (Breaking, Features, Fixes, Performance); if a subject reads badly, it is fixed in history only by the owner, never by a rewrite you start.
3. **Tests with the race detector.** `go test -race ./...` passes locally (CI runs the same on three OSes; `aval release` itself runs `go test ./...` without `-race`). Also `go vet ./...` and `gofmt -l .` empty.
4. **GoReleaser pin.** `.github/workflows/release.yml` pins `GORELEASER_VERSION` and `GORELEASER_SHA256` (the hash of `goreleaser_Linux_x86_64.tar.gz` from that release's `checksums.txt`). Upgrade only deliberately, in its own commit, after `goreleaser release --snapshot --clean --skip=publish`.
5. **Status and dry run.** `aval release status`, then the chosen command with `--dry-run`: check the version (before 1.0, `feat` or breaking bumps the minor, `fix`/`perf` the patch; `docs`, `test`, `ci`, `chore` alone mean nothing to publish).
6. **Tag (authorized only).** The cutting command: it checks clean tree, `main`, up to date, `go test ./...`, green CI on `HEAD` when `gh` is available, shows the notes, asks `y/N`, tags and pushes the tag. `promote` re-tags the rc's commit: it requires the rc to be an ancestor of `origin/main`, skips the branch and up-to-date checks, and checks CI on the rc. If `main` moved, it lists the later commits and warns when any changes shipped code (outside `docs/`, `tests/`, `odd/`, `.claude/`, `*.md`); cut a new rc then.
7. **Verify.** The workflow URL it prints: `preflight`, `publish` (on its own unless the tag opens a breaking line, then after the owner approves the environment), `verify`, `npm`. Then by hand:

```bash
gh release download vX.Y.Z -R alvaroofernaandez/aval
shasum -a 256 -c SHA256SUMS --ignore-missing      # Linux: sha256sum -c
gh attestation verify aval_X.Y.Z_<os>_<arch>.tar.gz --repo alvaroofernaandez/aval
tar -xzf aval_X.Y.Z_<os>_<arch>.tar.gz && ./aval version
npx @alvaroofernaandez/aval@next version          # rc/beta; @latest for stable
```

8. **Release body (after publish).** Read GoReleaser's list with `gh release view vX.Y.Z-rc.N --json body -q .body`, then `gh release edit vX.Y.Z-rc.N --notes-file <file>` where the file is the English notes, then the Spanish notes, then that generated list. Relative links and images in the notes must be rewritten first to absolute `https://github.com/alvaroofernaandez/aval/blob/<tag>/...` and `https://raw.githubusercontent.com/alvaroofernaandez/aval/<tag>/...` URLs (details in `docs/releasing.md`), and Mermaid diagrams replaced with tables, because a release body does not render Mermaid. Editing a release body is a remote action: only with the owner's authorization.

## If something fails

Follow `docs/releasing.md`, "If something fails". Deleting a remote tag (`git push origin :refs/tags/<tag>`) is a remote action: only with the owner's authorization, and only before anything was approved.

## Mechanisms behind this checklist

- `internal/release` (`internal/release/git_test.go`): the preflight checks, the version arithmetic and the notes grouping.
- `cmd/aval/release_test.go`: the command wiring.
- ADR 0003: CI, not pre-push, runs the tests; a release requires CI green on the tagged commit.

## Report

The version, each checklist step with its command and result, what was not run and why, and the exact point you stopped for authorization.
