---
name: vesper-release-distribution
description: "Use this skill to ship, rerun, or debug a Vesper desktop release using the current package-version-driven workflow: validate `apps/electron/package.json`, keep required release version markers in sync, inspect the desktop `prepare-release` gate, verify release artifacts, publish or update the GitHub release, and confirm mirroring to `sipherxyz/vesper-internal-release`."
---

# Vesper Release Distribution

Use this skill for Vesper desktop release operations in `sipherxyz/vesper`.

Follow the current release architecture exactly:

1. `apps/electron/package.json` is the version source of truth.
2. Shared release markers such as `packages/shared/src/version/app-version.ts` must stay in sync with the package version when present.
3. `.github/workflows/desktop.yml` decides whether a release should run via `prepare-release`.
4. Platform builds run only when `should_release == true`.
5. Packaged artifacts are verified before publication.
6. The GitHub Release in `sipherxyz/vesper` is the source release.
7. `.github/workflows/publish-internal-release.yml` mirrors binaries + notes to `sipherxyz/vesper-internal-release`.

Do **not** use the old mental model of pushing a separate `release` branch.

## When To Use

Use this skill to:

- ship a new desktop release from a version bump
- verify whether a version bump should release
- rerun publication for an existing tag
- diagnose why a release skipped, failed, or only partially published
- verify source release + internal mirror correctness

## Read First

Before acting, read:

- `.github/workflows/desktop.yml`
- `.github/workflows/publish-internal-release.yml`
- `apps/electron/package.json`
- `scripts/verify-release-assets.mjs`
- `scripts/generate-release-notes.mjs`
- `scripts/generate-electron-update-manifest.mjs`

## Required Outputs

A release is not complete unless these artifacts exist where expected.

### Packaged binaries
- `Vesper-arm64.dmg`
- `Vesper-x64.dmg`
- `Vesper-x64.exe`
- `Vesper-x86_64.AppImage`

### Installer/update helpers
- `scripts/install-app.sh`
- `scripts/install-app.ps1`

### Mirror expectations
The internal mirror must preserve:
- the same packaged binaries
- release title / notes parity
- prerelease flag parity when applicable

## Primary Procedure

### A. Ship a new release

1. Confirm repo, branch policy, and working-tree safety.
2. Read `apps/electron/package.json` and identify the target version.
3. Inspect `desktop.yml` precheck logic before assuming a release will run.
4. Push the version bump through the repo’s release-authorized branch flow.
5. Watch `desktop.yml` and inspect `prepare-release` outputs:
   - `version`
   - `tag`
   - `should_release`
6. If `should_release` is `true`, monitor:
   - macOS arm64 build
   - macOS x64 build
   - Windows installer build + smoke test
   - Linux AppImage build
7. Verify artifact collection and `verify-release-assets.mjs` success.
8. Verify GitHub Release creation/update succeeded.
9. Verify update manifest generation + deployment succeeded.
10. Verify `publish-internal-release.yml` ran and the mirrored release exists.

### B. Rerun publication for an existing tag

Use this path when assets, notes, or mirror state must be repaired without minting a new version.

1. Confirm the target tag points at the expected commit.
2. Trigger the supported rerun path for `desktop.yml`.
3. Use workflow rerun semantics rather than hand-creating or moving tags.
4. Re-verify source release assets, notes, update manifest, and internal mirror state.

### C. Diagnose a skipped or failed release

Always classify the problem before fixing it.

#### 1. Precheck failure / skip
Check:
- package version source
- previous version at `github.event.before`
- existing remote tag state
- `should_release`

Typical causes:
- version did not change
- tag already exists on the same commit and no forced rerun was intended
- tag exists on a different commit and the workflow correctly refused reuse
- release was intentionally gated off

#### 2. Build failure
Check:
- macOS matrix outputs
- Windows installer build
- Windows smoke test
- Linux AppImage build
- artifact upload/download paths

Typical causes:
- one platform packaging job failed
- artifact path mismatch
- Windows smoke failure

#### 3. Publish failure
Check:
- tag creation / reuse path
- release notes generation
- GitHub Release create/edit step
- asset upload step
- update manifest generation/deploy

Typical causes:
- tag conflict
- notes generation issue
- asset upload mismatch
- Pages deployment issue

#### 4. Mirror failure
Check:
- `publish-internal-release.yml` trigger
- source asset download
- mirrored release recreation logic
- notes / prerelease parity in target repo

Typical causes:
- mirror workflow never triggered
- source release missing expected assets
- target repo token/permission issue
- mirrored release recreation failed

## Operating Rules

- Follow the workflow; do not invent a parallel release path unless the user explicitly asks for emergency repair.
- Package version is authoritative.
- Artifact verification is mandatory.
- `vesper-internal-release` is a mirror stage, not the source publication stage.
- Preserve tag integrity. If a tag exists on a different commit, stop and surface it clearly.
- Start release investigation at `prepare-release`, not at downstream build jobs.

## Recommended Checks

### Repository state
- confirm target branch policy
- confirm repo remote
- confirm `apps/electron/package.json` version

### Workflow state
- inspect latest `desktop.yml` run
- inspect `prepare-release` summary
- inspect per-platform build jobs
- inspect release job logs
- inspect `publish-internal-release.yml` run history

### Release state
- inspect GitHub Release by tag
- verify uploaded assets
- verify release notes presence
- verify update manifest publication
- inspect mirrored release in `sipherxyz/vesper-internal-release`

## Useful Commands

Use GitHub CLI as the primary interface.

### View workflow and runs
```bash
gh workflow view desktop.yml --repo sipherxyz/vesper
gh run list --workflow desktop.yml --repo sipherxyz/vesper
gh run view <run-id> --repo sipherxyz/vesper --log
gh run watch <run-id> --repo sipherxyz/vesper
```

### Manual rerun / mirror
```bash
gh workflow run desktop.yml --repo sipherxyz/vesper -f force=true
gh workflow run publish-internal-release.yml --repo sipherxyz/vesper -f tag=vX.Y.Z
```

### Release inspection
```bash
gh release view vX.Y.Z --repo sipherxyz/vesper
gh release view vX.Y.Z --repo sipherxyz/vesper-internal-release
gh release download vX.Y.Z --repo sipherxyz/vesper --dir /tmp/vesper-release-assets
```

## Preconditions

- Run from the Vesper repo root when doing local validation.
- `gh` must be authenticated for `sipherxyz/vesper`.
- `gh` access must also cover `sipherxyz/vesper-internal-release` when validating the mirror.
- `node`, `bun`, `git`, and `gh` must be available when reproducing release checks locally.
- The operator should know whether they are shipping a new version or rerunning publication for an existing one.

## Done Criteria

### New release
- target version confirmed from `apps/electron/package.json`
- related release version markers kept in sync where required
- `desktop.yml` precheck decision understood
- build jobs complete successfully
- required artifacts verified
- GitHub Release present and correct
- update manifest published
- internal mirror present and correct

### Rerun / repair
- target tag confirmed
- rerun path clearly identified
- source release corrected
- mirror corrected if needed
- no tag-integrity regression introduced

### Investigation
- failing stage identified precisely
- evidence captured from workflow/run/release state
- next action specific and actionable

## Anti-Patterns

Avoid:

- assuming a release should happen just because a workflow started
- assuming build success means publish success
- debugging the internal mirror before checking the source release
- treating `release` branch workflows as current architecture
- manually moving tags to “unstick” a release without explicit approval
- skipping the `prepare-release` gate analysis

## Install Or Update (optional)

```bash
bun run scripts/install-skill-from-dir.ts \
  --src skills/vesper-release-distribution \
  --dest ~/.claude/skills \
  --force
```
