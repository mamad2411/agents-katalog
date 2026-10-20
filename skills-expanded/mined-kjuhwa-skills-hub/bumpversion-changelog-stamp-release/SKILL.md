---
name: bumpversion-changelog-stamp-release
description: Finalize a release by stamping the changelog, running bumpversion across all tracked files, and creating a signed tag — without pushing.
category: agents
version: 1.0.0
version_origin: extracted
tags: [release, bumpversion, changelog, semver, git-tag]
source_type: extracted-from-git
source_url: https://github.com/jamiepine/voicebox.git
source_ref: main
source_commit: 476abe07fc2c1587f4b3e3916134018ebacd143d
source_project: voicebox
confidence: high
imported_at: 2026-04-18T00:00:00Z
---

# Bumpversion changelog-stamp release

## When to use
Cutting a new release from a mature `[Unreleased]` draft. You want version bumps synchronized across every tracked file (Cargo.toml, tauri.conf.json, package.json family, backend `__init__.py`, etc.), a stamped changelog section, one commit, and one tag — ready to push when you decide.

## Steps
1. Verify the working tree is clean except for `CHANGELOG.md` (`git status --porcelain`). If anything else is dirty, stop and have the user commit or stash — you don't want unrelated changes in a release commit.
2. Read the current version from `.bumpversion.cfg` (`grep '^current_version' .bumpversion.cfg`). Ask the user (or infer) the bump level: `patch`, `minor`, `major`. Compute the next version.
3. Stamp the changelog manually:
   a. Insert a new `## [X.Y.Z] - YYYY-MM-DD` heading directly after `## [Unreleased]`.
   b. Move the body that was under `[Unreleased]` into the new stamped section.
   c. Leave `[Unreleased]` with an empty body so the next development cycle starts clean.
   d. Update the reference links at the bottom: change `[Unreleased]` to `compare/vX.Y.Z...HEAD`; add `[X.Y.Z]: compare/vPREVIOUS...vX.Y.Z`.
4. `git add CHANGELOG.md`. The changelog is now staged.
5. Run `bumpversion --allow-dirty <level>`. `--allow-dirty` is required because CHANGELOG.md is already staged. bumpversion updates every file listed in `.bumpversion.cfg`, creates a single commit (message format is `Bump version: X.Y.Z -> A.B.C`), and tags it `vA.B.C`. The staged changelog rides along in that commit.
6. Verify: `git show --name-only --stat HEAD` should list `CHANGELOG.md`, `.bumpversion.cfg`, tauri/Cargo/package files, and backend/__init__.py. `git tag --list "v*" --sort=-v:refname | head -n 5` should show the new tag at the top.
7. **Do not push.** Report the tag and suggest `git push origin main --follow-tags` when the user is ready.

## Counter / Caveats
- Never amend a release commit that has been pushed. To undo locally: `git tag -d vX.Y.Z && git reset --soft HEAD~1`.
- Don't override the bumpversion commit message; downstream CI often parses the canonical format.
- If the release CI extracts release notes from CHANGELOG.md (by matching the `## [X.Y.Z]` heading), stamp the exact version string — typos become empty release pages.
- If bumpversion fails partway, the tag won't exist. Fix the cause and re-run — the step is idempotent as long as the tag is absent.
- Run `draft-release-notes` first to make sure the `[Unreleased]` body reflects reality before stamping.

Source references: `.agents/skills/release-bump/SKILL.md` (the full workflow this skill extracts), `.bumpversion.cfg`, `CHANGELOG.md`.
