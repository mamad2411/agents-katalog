---
name: release
description: Cut a toolpass release now (choose the version, check main is green, start the release workflow, verify the Python packages, image, chart and npm package). Use when asked to release, publish or tag a version.
---

# Releasing toolpass

Releases normally happen on their own: `.github/workflows/daily-release.yaml` runs at 03:00 UTC and
releases `main` as the next patch version when it changed since the last tag and CI passed on it.
Use this skill for a release now, or for a minor or major bump.

## 1. Decide the version

- `git fetch --tags origin` and list what changed since the latest `vX.Y.Z` tag:
  `git log --oneline <last>..origin/main`.
- Nothing since the last tag: stop and say so.
- While the version is 0.x: **minor** (`0.2.0`) when a user-visible feature or a breaking change
  landed (new command, new integration, changed config or API), **patch** (`0.1.1`) for fixes,
  docs and examples only. The person asking may name the version; use it.

## 2. Check main is releasable

- The latest `ci` run on `main` (event `push`) for the head commit must be `completed success`.
  If it is red or still running, fix or wait; never release a red `main`.
- A failing nightly run on `main` (the long property tests) is a bug to fix first, not a reason to skip.

## 3. Start the release

Run the `release` workflow on `main` with `version: vX.Y.Z` (GitHub Actions `run_workflow`, or
Actions → release → Run workflow). For a minor or major bump you can also run `daily-release` with
`bump: minor|major`, which does the checks above itself.

## 4. Verify

The release workflow builds everything from the tag: `tag`, then `image`, `chart`, `assets`,
`pypi` and `npm`. `.github/scripts/build-python.sh` sets the version of `toolpass` (toolpass-py).

- The run's `tag`, `image`, `chart`, `assets`, `pypi` and `npm` jobs all succeed; if one fails,
  read its log and fix.
- `ghcr.io/roee-hersh/toolpass:<version>` and `:latest` exist (linux/amd64 and linux/arm64), and
  `docker run --rm ghcr.io/roee-hersh/toolpass:<version> version` prints the version.
- `helm show chart oci://ghcr.io/roee-hersh/charts/toolpass --version <version>` works without
  logging in.
- The `pypi` and `npm` jobs succeeded, not skipped (skipped means the `PUBLISH_PYPI` or
  `PUBLISH_NPM` variable is unset), and the registries serve the new version:
  `https://pypi.org/pypi/toolpass/json` and `https://registry.npmjs.org/toolpass-client`. The docs tell users to install from them, so a
  missing version is a failed release.
- The `assets` job succeeded and the release lists `toolpass-python.tar.gz`,
  `toolpass-client-node.tgz`, the wheel `toolpass-<version>-py3-none-any.whl` and `checksums.txt`.

Reply with the release link, the version, and a short list of what it contains (PR titles).
