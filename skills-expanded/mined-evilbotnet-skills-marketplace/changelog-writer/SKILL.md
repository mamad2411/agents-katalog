---
name: changelog-writer
description: Generate or update CHANGELOG.md in Keep a Changelog format from git history since the last release. Use when the user asks to write, update, or draft a changelog or release notes.
---

# Changelog Writer

Maintain CHANGELOG.md in [Keep a Changelog](https://keepachangelog.com)
format, written for users of the project — not a commit log dump.

## Procedure

1. Find the last release: latest semver tag (`git describe --tags
   --abbrev=0`) or the newest version heading in CHANGELOG.md. List
   commits since then (`git log <tag>..HEAD --oneline`).
2. Read beyond subjects when a commit is unclear — check the diff stat or
   body. Group user-visible changes under: **Added**, **Changed**,
   **Deprecated**, **Removed**, **Fixed**, **Security**.
3. Rewrite for the reader: "Added `--no-sync` flag to skip marketplace
   refresh on launch", not "feat: add nosync flag". Omit internal-only
   changes (refactors, CI tweaks) unless they affect users.
4. Version: if the user named one, use it; otherwise propose by semver
   (breaking → major, features → minor, fixes only → patch) and say why.
5. Insert the new section above the previous release, dated today, in the
   existing file's style. Create the file with the standard preamble if
   missing. Never rewrite released sections.

Show the diff before writing if the changelog already exists.
