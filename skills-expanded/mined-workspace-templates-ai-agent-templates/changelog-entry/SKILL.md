---
name: changelog-entry
description: Builds a Keep a Changelog entry from the commits since the last tag and adds it to CHANGELOG.md after you approve the text.
disable-model-invocation: true
---

Draft a changelog entry. Version requested: $ARGUMENTS (suggest one if empty).

1. Find the last tag with `git describe --tags --abbrev=0`. If none exists, use the first commit. List `git log <tag>..HEAD --no-merges` and read the diff of any commit whose subject is unclear.
2. Group changes under **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security**. Omit empty groups.
3. Write each line from the user's point of view, in the past tense, one sentence, with the pull request or issue number if the commit has one. Skip refactors, tests, CI and formatting unless users notice.
4. Suggest the version: major for a breaking change, minor for Added, patch otherwise. Explain the choice in one line.
5. Use the heading `## [x.y.z] - YYYY-MM-DD` with today's date, and keep the style of the existing CHANGELOG.md.

Show the entry and ask for approval. Only then insert it below the Unreleased heading. Never create the tag.
