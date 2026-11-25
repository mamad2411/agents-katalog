---
name: release-publish
description: Use when publishing MCP Manager desktop releases from this repository, especially when the version should default to the next patch release and the flow should run end-to-end through GitHub Releases.
---

# Release Publish

## When to Use

- The release-ready code is already committed locally.
- The release should usually use the next stable patch version.
- The GitHub draft release should be published automatically after the workflow succeeds.

## Preconditions

- Run from the repository root.
- The git working tree must be clean before starting.
- The current branch should be `main` unless you intentionally override it.
- `gh auth status` should already succeed with push access to `xjeway/mcp-manager`.

## Default Command

```bash
python3 plugins/release-publisher/scripts/publish_release.py
```

This command:

- reads the current project version
- chooses the next patch version by default
- runs `make release-prepare`
- commits and pushes the release bump
- runs `make release-publish`
- waits for `.github/workflows/release.yml`
- publishes the draft GitHub Release
- verifies `releases/latest/download/latest.json`

## Overrides

Use an explicit version when you do not want the next patch or when the current version is already a prerelease:

```bash
python3 plugins/release-publisher/scripts/publish_release.py --version 0.2.0
```

Use `--dry-run` to resolve the next version and repository context without making changes:

```bash
python3 plugins/release-publisher/scripts/publish_release.py --dry-run
```

## Failure Model

- Stop immediately on a dirty worktree, tag collision, push failure, workflow failure, or invalid updater manifest.
- Do not manually delete release assets before rerunning.
- Fix the root cause and rerun the script from a clean repository state.
