---
name: publish-release
description: Publish this npm package through the tag-triggered release workflow with changelog-backed GitHub Release notes. Use when user says "publish release", "publish npm package", "npm release", "create release", or wants to ship a new package version.
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Publish Release

Publish this package with npm Trusted Publishing and a matching GitHub Release.

Read `PUBLISHING.md` first for the authoritative release contract.

## Instructions

### Step 1: Confirm Release Intent

Confirm the user explicitly asked to publish or prepare a release. Do not
publish, tag, deprecate, or push release refs from a vague request.

Identify whether the release should be:

- stable: publishes to npm `latest` and creates a normal GitHub Release;
- prerelease: publishes to npm `next` and creates a GitHub prerelease.

### Step 2: Inspect Repository State

Check the current branch, local status, recent commits, npm package version, npm
dist-tags, and existing git tags. Pull the latest target branch before tagging.

If unrelated local changes exist, commit only the release-related changes or ask
how they should be handled. Never discard user-owned work.

### Step 3: Prepare Release Notes

Update `CHANGELOG.md` before running `npm version`:

- keep an empty `## Unreleased` heading at the top;
- add `## <version> - YYYY-MM-DD` for the version being released;
- move the release content under that exact version heading;
- include user-facing release notes for features, fixes, breaking changes,
  migrations, and operational changes.

Run the changelog extraction script for the intended version and verify it
prints the notes that should appear on the GitHub Release:

```bash
node scripts/extract-changelog-release-notes.mjs <version>
```

### Step 4: Verify The Package

Run the release gate:

```bash
pnpm install --frozen-lockfile
pnpm verify
```

Do not continue if verification fails.

### Step 5: Create The Version Commit And Tag

Use npm's version command so `package.json`, `pnpm-lock.yaml`, the release
commit, and the git tag stay aligned:

```bash
npm version patch
```

Use `minor`, `major`, or `prerelease --preid beta` when that matches the release
intent.

### Step 6: Push And Monitor

Push the branch and tag together:

```bash
git push origin main --follow-tags
```

Monitor the `Publish npm` workflow. It must:

- verify the tag matches `package.json`;
- publish to npm with the correct dist-tag, or skip if already published;
- extract release notes from `CHANGELOG.md`;
- create or update the GitHub Release for the same tag.

### Step 7: Confirm The Published Release

After the workflow completes, check:

- npm reports the expected version on `latest` or `next`;
- the GitHub Release exists for the same tag;
- release notes match the changelog section;
- a quick installed-package smoke test works when appropriate.

## Critical Rules

- Git tags are the release trigger and source of truth.
- GitHub Releases are created by the tag workflow, not manually before tagging.
- Release notes come from `CHANGELOG.md`, not from ad hoc workflow text.
- Do not publish from a dirty or unverified tree.
- Do not force-push or reuse npm versions.

## Checklist

- [ ] Read `PUBLISHING.md`
- [ ] Confirmed stable vs prerelease intent
- [ ] Pulled the latest target branch
- [ ] Updated `CHANGELOG.md` with the exact version heading
- [ ] Checked extracted release notes
- [ ] Ran `pnpm install --frozen-lockfile`
- [ ] Ran `pnpm verify`
- [ ] Ran the correct `npm version` command
- [ ] Pushed `main` and tags together
- [ ] Confirmed npm package and GitHub Release are in sync

## Reference

- `PUBLISHING.md` -- release process and npm Trusted Publishing setup
- `CHANGELOG.md` -- release note source for npm and GitHub releases
- `.github/workflows/publish-npm.yml` -- tag-triggered npm and GitHub Release workflow
- `scripts/extract-changelog-release-notes.mjs` -- release note extraction script
