---
name: multi-platform-desktop-release-workflow-github-actions
description: Build and sign desktop apps (macOS, Windows, Linux) from a single CI workflow with conditional code-signing
category: ci
version: 1.0.0
version_origin: extracted
confidence: high
tags: [ci, release, desktop, github-actions]
source_type: extracted-from-git
source_url: https://github.com/pingdotgg/t3code.git
source_ref: main
source_commit: 9df3c640210fecccb58f7fbc735f81ca0ee011bd
source_project: t3code
imported_at: 2026-04-18
evidence:
  - .github/workflows/release.yml
  - docs/release.md
  - .docs/scripts.md
---

## When to Apply
- You build Electron apps for macOS (arm64 + x64), Windows (x64), and Linux
- You want a single release workflow triggered by git tags (`v*.*.*`)
- You need code-signing and notarization for macOS and Windows
- You support nightly builds on a schedule (e.g., every 3 hours)
- You want to conditionally enable signing only when secrets are present

## Steps
1. Add `release.yml` with three trigger types: tag push (`v*.*.*`), schedule (`0 */3 * * *`), and workflow_dispatch
2. First job: `check_changes` — on schedule, compare HEAD to last nightly tag; skip if no changes
3. Second job: `preflight` — sets release metadata (version, channel, tag); depends on check_changes
4. Platform-specific jobs: `build-macos`, `build-windows`, `build-linux` — depend on preflight
5. Conditionally enable signing with `secrets.APPLE_*` (macOS) and `AZURE_TRUSTED_SIGNING_*` (Windows)
6. Publish artifacts to GitHub Releases with version/channel metadata
7. For nightly, use `-nightly` tag suffix and set `is_prerelease: true`
8. For stable, set `make_latest: true` to mark as latest in GitHub UI

## Example
```yaml
on:
  push:
    tags: ['v*.*.*']
  schedule:
    - cron: '0 */3 * * *'

jobs:
  preflight:
    runs-on: blacksmith-8vcpu-ubuntu-2404
    outputs:
      version: ${{ steps.release_meta.outputs.version }}
  build-macos:
    needs: preflight
    runs-on: macos-latest
    steps:
      - run: bun run dist:desktop:dmg:arm64
      - if: secrets.APPLE_ID
        run: codesign -s "${{ secrets.APPLE_CERT_ID }}" dist.dmg
  publish:
    needs: [build-macos, build-windows, build-linux]
    runs-on: ubuntu-latest
    steps:
      - uses: softprops/action-gh-release@v1
        with:
          files: release/*
```

## Counter / Caveats
- Apple notarization can be slow (5-10min); plan CI timeout accordingly
- Azure Trusted Signing requires service principal setup; test with `--dry-run` first
- GitHub release secrets are not exposed to pull requests; tag-based releases work, but workflow_dispatch won't sign in PRs
- Nightly builds consume GitHub Actions minutes; throttle to every 3 hours or longer
- Unsigned releases are shareable but may trigger OS warnings on first launch
