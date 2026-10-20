---
name: draft-release-notes-from-git-log
description: Keep a non-destructive [Unreleased] changelog draft in sync with the actual diff since the last tag, using git log + GitHub's generate-notes API.
category: agents
version: 1.0.0
version_origin: extracted
tags: [changelog, releases, git, github-cli, documentation]
source_type: extracted-from-git
source_url: https://github.com/jamiepine/voicebox.git
source_ref: main
source_commit: 476abe07fc2c1587f4b3e3916134018ebacd143d
source_project: voicebox
confidence: high
imported_at: 2026-04-18T00:00:00Z
---

# Draft release notes from git log

## When to use
You maintain a human-readable `CHANGELOG.md` (Keep-a-Changelog style) and want the `[Unreleased]` section to stay honest during development so it's one command away from being stamped into a release.

## Steps
1. Detect the last tag: `LAST_TAG=$(git tag --list "v*" --sort=-v:refname | head -n 1)`. This is the scope boundary for the draft.
2. Gather three raw inputs:
   - `git log --oneline "$LAST_TAG"..HEAD` — the actual commits in order.
   - `gh api repos/:owner/:repo/releases/generate-notes -f tag_name="vNEXT" -f target_commitish=$(git rev-parse HEAD) -f previous_tag_name="$LAST_TAG" --jq '.body'` — GitHub's auto-generated PR-title list.
   - `git diff --stat "$LAST_TAG"..HEAD` — which areas changed, for theme clustering.
3. Draft a narrative: one strong opening paragraph (what this release is about, why it matters, tied to concrete changes), one optional paragraph on major technical shifts, then themed bullet groups (`### Feature group`, `### Bug Fixes`) with PR links where known.
4. Replace **only** the body between `## [Unreleased]` and the next `## [` heading. Preserve the `[Unreleased]` heading itself so the file always has that section first after the header comments. Never touch stamped release sections.
5. Do not commit, tag, or bump. The draft lives as a dirty file in the working tree and can be regenerated freely — "non-destructive working copy".
6. If `git log "$LAST_TAG"..HEAD` is empty, leave the section empty and tell the caller there's nothing to draft.

## Counter / Caveats
- Be factual and specific — every claim must trace to a commit or PR. Fabricated "improvements" get flagged by maintainers.
- Lead with prose, not bullets. The narrative is what readers consume; bullets are supporting evidence.
- Skip trivial chores (typo fixes, CI tweaks) unless they're the bulk of the release — otherwise the notes bury the important work.
- Match the voice of previous entries in the same CHANGELOG — look at the last two stamped sections for tone.
- Downstream skills (release-bump) depend on this draft being up-to-date before stamping. Re-run whenever a meaningful PR lands.

Source references: `.agents/skills/draft-release-notes/SKILL.md` (the full workflow this skill extracts), `CHANGELOG.md` (the format target).
