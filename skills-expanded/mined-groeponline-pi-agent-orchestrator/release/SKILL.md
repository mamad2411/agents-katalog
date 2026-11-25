---
name: release
description: Cut a release of @groeponline/pi-agent-orchestrator to npmjs.org and GitHub. Use when publishing a new version, creating a release tag, or validating the canonical release workflow.
---

# Release — pi-agent-orchestrator

Canonical path: **Prepare Release** button → reviewed PR → manual squash merge → **Release** dispatch on `main`.

Do not `git tag` locally. Do not add a second npm or GitHub Packages publisher. Duplicate tag triggers can publish only part of a release.

Operator detail lives in [`.github/NPM_SETUP.md`](../../../.github/NPM_SETUP.md) and [`RELEASE.md`](../../../RELEASE.md).

## Automated flow

1. Before running the button for the next valid patch release (currently `0.19.1`), advance the pinned release workflow and policy in a dedicated reviewed change: the current source is `0.19.0`; the reviewed policy is pinned to the next patch before preparation.
2. Run the newly pinned **Prepare Release** workflow on `main` with its exact confirmation value. The workflow writes `package.json`, both lockfile root versions, `CHANGELOG.md`, and `showcase/remotion/public/promo-data.json`, then opens the matching release branch.
3. After that PR squash-merges, dispatch `release.yml` on `main`; it matches subject `chore(release): v$VERSION`.
4. It re-runs the immutable gate, publishes the packed tarball with provenance, then creates tag `v$VERSION` and the GitHub Release.

```text
prepare-release.yml (button on main)
→ reviewed PR with CHANGELOG.md + package.json + package-lock.json + showcase/remotion/public/promo-data.json
→ manual squash merge to main
→ dispatch release.yml → verify → npm publish --provenance → tag + GitHub Release
→ pages.yml (package.json/CHANGELOG.md path filters) republishes pi.video
```

## Before releasing

1. Confirm the intended commit is on `main` and required CI is green.
2. Check the currently published version:

   ```bash
   npm view @groeponline/pi-agent-orchestrator version
   ```

3. Keep `.release-policy.json` on the locked `0.19.x` train. `0.20.0` remains blocked and requires a dedicated policy change.
4. Ensure the package catalog contract passes:

   ```bash
   npm run verify:package
   npm pack --dry-run
   ```

## Authentication

Current publisher uses repository secret `NPM_TOKEN` plus `id-token: write` for provenance.

Preferred target is npm trusted publishing for `release.yml`. Do not remove token authentication until that publisher is verified.

## Post-release verification

```bash
npm view @groeponline/pi-agent-orchestrator version
npm view @groeponline/pi-agent-orchestrator pi --json
curl -sI "https://groeponline.github.io/pi-agent-orchestrator/assets/dashboard_preview.mp4"
pi -e npm:@groeponline/pi-agent-orchestrator
```

Confirm that:

- npm reports the intended version;
- `pi.extensions` includes `./dist/index.js`;
- `pi.video` is the public GitHub Pages MP4 and that URL returns `video/mp4`;
- the matching GitHub Release exists;
- GitHub Pages finished deploying (Actions → Deploy Pages);
- pi.dev shows `@groeponline/pi-agent-orchestrator`, not `@onlinechefgroep/...`.

A Pages-only asset fix does not need a version bump. npm README / `pi.*` metadata changes do.

## Recovery rules

- Never overwrite or reuse a published version.
- If npm succeeded and GitHub Release creation failed, re-run the failed Release job; do not republish.
- If npm failed, repair authentication or validation and release a new valid version.
- `dist/` is generated during publishing and must remain uncommitted.
