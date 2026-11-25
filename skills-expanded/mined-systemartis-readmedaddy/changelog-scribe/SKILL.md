---
name: changelog-scribe
description: >-
  Use when a release is being cut and the CHANGELOG is empty, stale, or out of
  sync with the commits since the last tag; when commit messages need to be
  turned into human-readable release notes grouped by type; or when asked to
  "update the changelog", "write release notes", or "what changed since the last
  release". Not a version bumper and not a tag/publisher; yields to an existing
  changelog format already in the repo.
license: MIT
metadata:
  version: 0.4.0
---

# changelog-scribe

changelog-scribe turns the commit range since the last release tag into a clean,
grouped CHANGELOG section: features, fixes, and breaking changes, each as a
reader-facing line rather than a raw commit subject. It follows Keep a Changelog
ordering and never invents an entry that has no commit behind it.

## Method

1. **Find the range.** Resolve the latest release tag and collect commits from
   that tag to `HEAD`. If there is no tag, use the full history and say so.
2. **Classify each commit.** Bucket into Added / Changed / Fixed / Removed /
   Deprecated / Security from the commit type and body, dropping noise commits
   (merges, formatting-only, CI tweaks).
3. **Rewrite for readers.** Convert each kept commit into a present-tense, user-
   facing line. A commit subject is a developer note; a changelog line is for the
   person upgrading.
4. **Assemble the section.** Emit a dated `## [version]` block in the repo's
   existing changelog order, breaking changes first and called out explicitly.
5. **Verify.** Every line traces back to a real commit in the range. Nothing is
   added that the diff does not support.

## What's in references/

- `references/grouping.md` — the commit-type to changelog-section mapping and the
  noise-commit filter rules.
