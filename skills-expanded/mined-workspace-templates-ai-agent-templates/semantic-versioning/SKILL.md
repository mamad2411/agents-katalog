---
name: semantic-versioning
description: Works out the next version number from the real changes since the last tag, applies semver rules to breaking changes and drafts the release notes.
---

# Semantic versioning

Decide the bump from what consumers can observe, not from commit prefixes.

## Steps

1. Find the last release: `git describe --tags --abbrev=0` and its tag. If versions below 1.0.0, say so: 0.x allows breaking changes in minor releases, but still note them.
2. Read the change since then: `git diff <tag>..HEAD --stat` and the diff of every file that is part of the public surface (exports, CLI flags, config keys, HTTP routes, database or file formats, environment variables).
3. Classify each change:
   - **Major**: removed or renamed public item, changed argument order or type, narrower accepted input, different return shape, changed default that alters results, dropped runtime or platform support, new required config.
   - **Minor**: new optional feature, new export, wider accepted input, new optional field, deprecation (with the old path still working).
   - **Patch**: bug fix that restores documented behavior, performance work, internal refactor, docs.
4. The highest class wins. A fix that changes behavior people relied on is a major, even if it was a bug.
5. Check internal consistency: update the version in every place it lives (`package.json`, lockfile, `pyproject.toml`, `Cargo.toml`, a version constant), the changelog, and any migration note a major bump needs.
6. Pre-releases use `-rc.1` style suffixes; build metadata uses `+` and never affects ordering.

## Rules

- Do not create the tag or publish. Propose the version and the file edits.
- If a change is ambiguous, list it under "judgment calls" and choose the higher bump.

## Report

The version, the list of changes grouped by class with the file for each, the judgment calls, and draft release notes written for users.
