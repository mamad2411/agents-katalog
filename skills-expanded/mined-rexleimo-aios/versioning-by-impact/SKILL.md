---
name: versioning-by-impact
description: Use when completing a task and deciding whether repository changes require a semantic version bump and changelog entry before commit/push.

installCatalogName: versioning-by-impact
clients: [codex, claude, gemini, opencode, hermes, workbuddy, pi, zcode, qoder]
scopes: [global, project]
defaultInstall:
  global: true
  project: false
tags: [general, release]
repoTargets: [codex, claude, gemini, opencode, hermes, workbuddy, pi, zcode, qoder]
---

# Versioning by Impact

## Overview
Apply Semantic Versioning decisions from actual change impact, not from task size.

## Impact Rules

- `none`: no repository file changes.
- `patch`: backward-compatible fixes, docs updates, translation/content updates, non-breaking refactors.
- `minor`: backward-compatible new features or new capabilities.
- `major`: any breaking change to CLI behavior, config contract, file layout contract, or documented usage.

## Release Ordering (submodule first)

A host release archives the `rex-harness` submodule work tree, so the version it
announces only exists if that submodule commit is itself a published
(tarball-bearing) rex-harness release.

- Release rex-harness first: tag `vX.Y.Z`, push, let its release workflow produce
  the GitHub Release asset. Then cut the host release whose gitlink points at
  that tagged commit.
- Never cut a host release over an untagged submodule commit. The host changelog
  would cite a rex-harness version that exists nowhere on the rex-harness remote,
  standalone rex-harness consumers get nothing, and the bundled kernel cannot be
  traced back to a release point.
- If an already-published host release turns out to cite an untagged submodule
  version, retroactively tag and release that submodule commit: the gap is a
  traceability defect in shipped artifacts, not a cosmetic one.

The gate is enforced by `scripts/release-preflight.sh` (and the `.ps1` twin) via
`scripts/check-release-submodule.mjs`; it fails closed when the tag state cannot
be proven.

## Required Output Format

Always report these 4 fields in final handoff:

1. `Version Impact: none|patch|minor|major`
2. `Recommended Version: vX.Y.Z -> vA.B.C` (or `no change`)
3. `Why: <one-sentence reason>`
4. `Release Notes:` short bullet list

When a release is requested, also state whether the submodule commit is already a
published rex-harness release, and in which order the two tags must go out.

## Repository Commands

- Read current version: `cat VERSION`
- Bump version + changelog entry: `scripts/release-version.sh <patch|minor|major> "summary"`
- Preview only: `scripts/release-version.sh --dry-run <patch|minor|major> "summary"`
- Refresh the machine-readable LLM index after any version/changelog/post change:
  `node scripts/generate-llms-txt.mjs` (verify only: add `--check`). `docs-site/llms.txt`
  is generated from `site-sources/llms.src.md` plus `VERSION`, `CHANGELOG.md` and
  `blog-site/*.md`; a hand-edited copy drifts (the live file once advertised v5.20.0
  while v6.2.0 was shipping, and listed 24 of 68 published posts).

## Default Behavior

If impact is `none`, do not bump version.
If impact is `patch|minor|major`, update both `VERSION` and `CHANGELOG.md` before commit.
