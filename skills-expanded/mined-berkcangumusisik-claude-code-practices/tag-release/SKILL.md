---
name: tag-release
description: Bumps version in package.json (or equivalent), creates a git tag, and pushes
argument-hint: <major|minor|patch> [--dry-run]
user-invocable: true
allowed-tools: Bash(git *) Read Edit
effort: low
---

## Create a Release Tag

Bump type: **$1** (major | minor | patch)

1. Get current version:
```bash
cat package.json | grep '"version"' | head -1
git tag --sort=-v:refname | head -5
```

2. Calculate new version based on semver and bump type `$1`.

3. Show what will happen:
   - Old version → New version
   - Files that will be modified
   - Tag that will be created

4. If `$ARGUMENTS` contains `--dry-run`, stop here.

5. Ask for confirmation, then:
   - Update version in `package.json` (or `pyproject.toml`, `Cargo.toml`, etc.)
   - Commit: `chore: bump version to X.Y.Z`
   - Tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`

6. Ask whether to push tag to remote.
