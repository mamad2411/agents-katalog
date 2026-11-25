---
name: bump-version
description: Use when the user asks to bump, set or raise the duolog version, or to
  prepare a release commit. Do not use to only check the version; check-version
  does that. Do not use to create a tag or publish a release.
compatibility: Requires uv and git. Run from the duolog repository.
argument-hint: "[version]"
arguments: [version]
---

# Bump the version

## Arguments

- `$version` - the new version, such as `1.2.3` or `1.2.3-rc.1`, with no `v`. When
  it is missing, ask for it in step 1.

## Communication

- Reply in the language the user writes in.
- Write files, comments and reports in English, ASCII only.
- Use simple English: short sentences, common words, simple grammar.

## Models

- The current model does all of it. The script writes the files, so a small model
  is enough.

## Before you start

- Run `uv --version`. If it fails, stop and ask the user to install uv:
  https://docs.astral.sh/uv/getting-started/installation/
- A sandbox can stop uv from writing its cache. If a later `uv run` reports that,
  set the variable `UV_CACHE_DIR` to `.cache/uv`, which git ignores, and run it
  again. Do not call Python directly, and do not edit the files by hand instead.
- Run `git status --short`. If it prints anything, stop and ask the user to commit
  or stash first. The bump must be an isolated diff.

## Steps

1. If `$version` is empty, ask: "Which version? Example: 1.2.3"

1. Read `## Development` in `CHANGES.md`. If it is empty, stop: a version with no
   entries has no release notes. Use the check-changes skill first.

1. Set the version. It moves the entries under the version, and prints the changed
   files as JSON.

   ```sh
   uv run scripts/version/version.py bump $version
   ```

   Exit 2 means the version is wrong. Exit 1 means that a place states no version
   or that `CHANGES.md` breaks a limit, and no file changed. In both cases, report
   the message and stop.

1. Check every place against the new version:

   ```sh
   uv run scripts/version/version.py check --tag v$version
   ```

1. Read `git diff`. Only the version and the new heading may change. If
   anything else changed, stop and report it.

1. Commit, if the user asked for a commit: `release: $version`. Do not tag and do
   not push. A person cuts the tag on `main`, after `develop` merges there, because
   the tag starts the release workflow and publishes the binaries.

## Done when

- `version.py check --tag v$version` exits with 0.
