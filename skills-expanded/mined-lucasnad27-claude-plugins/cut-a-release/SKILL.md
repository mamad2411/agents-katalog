---
name: cut a release
description: Use when cutting a release for a plugin in this claude-plugins marketplace repo. Triggers on phrases like "cut a release", "ship v1.2.3", "deploy to the marketplace", "bump the plugin version", or any request to publish/update a plugin for end users. Handles the dual-version-file gotcha (marketplace.json AND plugin.json must both be bumped) that otherwise silently breaks update detection.
allowed-tools:
  - Bash(git checkout:*)
  - Bash(git pull:*)
  - Bash(git status:*)
  - Bash(git log:*)
  - Bash(git diff:*)
  - Bash(git add:*)
  - Bash(git commit:*)
  - Bash(git push:*)
  - Bash(git tag:*)
  - Bash(git describe:*)
  - Bash(claude plugin tag:*)
  - Bash(gh pr create:*)
  - Bash(gh pr view:*)
  - Bash(gh pr merge:*)
  - Bash(gh release create:*)
  - Bash(gh release view:*)
  - Bash(ls:*)
  - Bash(sed:*)
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Cut a release for a plugin in this marketplace

This skill walks through releasing a plugin in the `claude-plugins` marketplace repo. The repo hosts multiple plugins; each has its own independent version. Releases are a git + GitHub affair — there's no build step or package registry to publish to. The "deploy" is just: bump versions, tag, push, and tell users to run `/plugin marketplace update`.

## The critical gotcha (read this first)

Every plugin has its **version declared in two separate files** that must stay in sync:

1. **`.claude-plugin/marketplace.json`** — the `version` field inside the matching entry in `plugins[]` (this is what Claude Code's update checker reads)
2. **`plugins/<plugin-name>/.claude-plugin/plugin.json`** — the plugin's own `version` field (this is what gets installed locally)

If these drift apart, Claude Code's `/plugin` will silently stop offering updates to users, even though the plugin code has moved on. Users appear stuck on an old version with no error message. **Always bump both in the same commit.**

## Step 0: Smoke-test main first

Don't bump a version you haven't run. Load the working tree into a real project for one
session — see `CLAUDE.md` for the `--plugin-dir` recipe and the name-collision footgun.

## Step 1: Determine version type

Based on changes since the last release, decide the SemVer bump:

- **MAJOR (X.0.0)** — Breaking changes to commands, skills, or agent interfaces; removed features; restructured workflow that existing users would need to relearn
- **MINOR (x.X.0)** — New commands, new skills, new agents, or new opt-in features
- **PATCH (x.x.X)** — Bug fixes, wording improvements, documentation fixes, small refinements to existing behavior

When in doubt for a plugin where users depend on muscle memory (command names, workflow steps), prefer MAJOR — being conservative here protects users.

## Step 2: Identify the target plugin and gather info

```bash
ls plugins/                    # list plugins in this marketplace
git status                     # confirm clean working tree
git log --oneline -20          # review recent changes
```

If tags exist for this plugin, review commits since the last release. Tag convention is
`<plugin-name>--vX.Y.Z`, matching what `claude plugin tag` generates. The per-plugin prefix
keeps plugins from colliding in a multi-plugin marketplace.

Tags through `research-plan-implement-v4.1.0` use a single dash and are left as they are —
their GitHub Releases hang off those exact names. The glob below matches both forms.

```bash
git describe --tags --abbrev=0 --match="<plugin-name>-*v*" 2>/dev/null  # latest tag for this plugin, if any
```

If no prior tag exists, review the full history of `plugins/<plugin-name>/` to craft release notes.

## Step 3: Prepare release branch

```bash
git checkout main
git pull origin main
git checkout -b release/<plugin-name>-vX.Y.Z
```

## Step 4: Bump both version files (the critical step)

**File 1**: `.claude-plugin/marketplace.json` — find the entry in `plugins[]` where `name` matches the plugin, and update its `version` field.

**File 2**: `plugins/<plugin-name>/.claude-plugin/plugin.json` — update the root `version` field.

After editing, verify the versions match:

```bash
grep '"version"' .claude-plugin/marketplace.json
grep '"version"' plugins/<plugin-name>/.claude-plugin/plugin.json
```

They MUST be identical strings. If they're not, the release is broken before it ships.

## Step 5: Update CHANGELOG

Each plugin keeps its own changelog at `plugins/<plugin-name>/CHANGELOG.md`. If none exists yet, create one using [Keep a Changelog](https://keepachangelog.com) format.

Add a new section at the top:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing behavior

### Fixed
- Bug fixes

### Removed
- Removed features (only in MAJOR bumps)
```

Only include sections that apply. Keep entries terse, user-facing, and impact-focused. Skip internal refactors unless users will feel them.

## Step 6: Commit, push, open PR

```bash
git add .claude-plugin/marketplace.json plugins/<plugin-name>/.claude-plugin/plugin.json plugins/<plugin-name>/CHANGELOG.md
git commit -m "chore(<plugin-name>): release vX.Y.Z"
git push -u origin release/<plugin-name>-vX.Y.Z
gh pr create --title "Release <plugin-name> vX.Y.Z" --body "$(sed -n '/## \['"X.Y.Z"'\]/,/## \[/p' plugins/<plugin-name>/CHANGELOG.md | sed '$d')"
```

The PR body is pulled from the CHANGELOG entry so reviewers see exactly what ships.

## Step 7: Wait for merge

**ACTION REQUIRED**: Stop here and wait for the user to confirm the PR has been reviewed and merged into `main`. Do not tag before merge — tags on unmerged branches cause confusion downstream.

## Step 8: Tag and push

After the PR is merged:

```bash
git checkout main
git pull origin main
claude plugin tag plugins/<plugin-name> --push -m "Release <plugin-name> v%s"
```

`claude plugin tag` re-checks that `plugin.json` and the marketplace entry agree before it
tags, so it catches a botched Step 4 at the last moment. Run it with `--dry-run` first if you
want to see the tag name without creating it.

## Step 9: Create GitHub Release

```bash
gh release create <plugin-name>--vX.Y.Z \
  --title "<plugin-name> vX.Y.Z" \
  --notes "$(sed -n '/## \['"X.Y.Z"'\]/,/## \[/p' plugins/<plugin-name>/CHANGELOG.md | sed '$d')"
```

## Step 10: Tell users how to update

Share these commands with users (or post in the release notes):

```
/plugin marketplace update research-plan-implement-workflow
/plugin
```

Then in the `/plugin` UI: Manage → select the plugin → Update.

The first command refreshes the marketplace manifest cache (this is where the dual-version-file fix takes effect — if marketplace.json wasn't bumped, `/plugin` won't see the new version). The second opens the plugin manager to apply the update.

## Quick reference: release checklist

- [ ] Smoke-tested from the working tree in a real project
- [ ] Version type decided (MAJOR/MINOR/PATCH)
- [ ] Release branch created from fresh `main`
- [ ] `marketplace.json` plugin entry version bumped
- [ ] `plugins/<name>/.claude-plugin/plugin.json` version bumped
- [ ] Both versions verified identical
- [ ] CHANGELOG updated with dated entry
- [ ] PR opened with CHANGELOG entry as body
- [ ] PR merged
- [ ] Tag `<plugin-name>--vX.Y.Z` created and pushed
- [ ] GitHub Release created
- [ ] Update instructions shared with users
