---
name: changelog-writer
description: Writes a changelog entry from the staged git diff. Use when asked to draft release notes.
---

# Changelog writer

Summarise the staged changes as a short changelog entry.

1. Run `git diff --staged` and read the output.
2. Group changes under Added, Changed and Fixed.
3. Follow the format described at https://keepachangelog.com/en/1.1.0/ when in doubt.

The entry template is pinned to a fixed commit:
https://raw.githubusercontent.com/olivierlacan/keep-a-changelog/0123456789abcdef0123456789abcdef01234567/CHANGELOG.md

To lint the result, run `npx markdownlint-cli@0.41.0 CHANGELOG.md`.
