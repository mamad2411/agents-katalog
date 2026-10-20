---
name: release-notes-automation
description: "Keep the CHANGELOG accurate between releases: check git tags, categorize new commits, fix stale sections, and commit. Scribe's primary release-notes workflow."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [changelog, release-notes, documentation, git-log, docs-lead]
    related_skills: [writing-plans, github, hermes-agent]
    triggers:
      - changelog
      - release-notes
      - git-log
      - version-tag
      - unreleased
      - docs-lead-pulse
      - documentation-review
      - release-automation
---

# Release Notes Automation

## Overview

Keep the project's CHANGELOG.md accurate between releases. The canonical changelog is at the repo root (`CHANGELOG.md`) and follows [Keep a Changelog](https://keepachangelog.com/) with date-based version tags (`vYYYY.M.D`).

This skill covers the periodic maintenance cycle: checking the latest tag, collecting new commits, resolving stale "Unreleased" sections, categorizing changes, and committing the update.

> **Support file:** `references/skill-content-dedup-workflow.md` — technique for extracting duplicate inline pitfall content that has matching reference files, replacing with links. Used during Scribe's skill-library hygiene campaigns.

## When to Use

- During a **docs-lead pulse** or any documentation review cycle
- When preparing **release notes** before a version tag
- When you notice the CHANGELOG has a stale "Unreleased" section that was actually released
- When you need to **audit what's landed since the last tag**
- After a **new version tag** has been pushed but the CHANGELOG wasn't updated

**Don't use for:**
- Writing implementation plans (`writing-plans` skill)
- Creating GitHub releases via `gh` CLI (`github` skill)
- Editing the website/docs site (that's Docusaurus)

## CHANGELOG Maintenance Workflow

### Step 1: Check the latest tag and recent commits

```bash
cd /path/to/repo

# Latest version tags
git tag -l 'v*' --sort=-v:refname | head -5

# Commits since the last tag
git log --oneline <latest-tag>..HEAD

# Or commits since a specific date
git log --oneline --since="2026-06-01"
```

### Step 2: Read the existing CHANGELOG

Read from the top of CHANGELOG.md — the Unreleased section is first.

Look for:
- Does `[Unreleased]` section exist? If yes, does it contain entries that match the current unreleased commits?
- Is a section labeled "Unreleased" that was *actually released* (i.e., a tag exists for that version)? If so, rename it.
- Is the CHANGELOG missing a tag section entirely? If so, create one.
- **Structural integrity check**: Scan for duplicate section headers (e.g., two `### Changed` blocks), missing blank lines between sections, or broken YAML frontmatter. Fix any structural defects found — they accumulate when multiple people edit the file.

### Step 3: Categorize commits by semantic type

Read the commit log and sort each commit into:

| Category | When to use |
|----------|-------------|
| **Added** | `feat:`, new features, new commands, new integrations |
| **Changed** | `refactor:`, behavior changes, deprecations (not new features) |
| **Fixed** | `fix:`, bug fixes, regressions corrected |
| **Removed** | Features deleted, env vars dropped, deprecated code stripped |

Respect the commit message types:
- `feat:` → Added
- `fix:` → Fixed
- `refactor:`, `change:` → Changed
- `docs:` → skip unless it's a major doc overhaul, then Changed
- `test:`, `chore:`, `style:`, `perf:` → skip minor, fold into Changed if user-visible

### Step 3.5: Cross-reference commits against existing entries

Before drafting, cross-reference each commit against what's already in `[Unreleased]`:

```bash
# When the last CHANGELOG entry was a date (no tag since):
git log --oneline --after="<date-of-last-changelog-entry>"

# Or when the Unreleased section was populated from a previous cycle:
# Compare each commit message against existing bullet descriptions
```

For each commit, check:
- Is this commit already represented in the existing `[Unreleased]` entries? If yes, skip it.
- Is this commit a new undocumented change? Draft a new entry (go to Step 4).
- Does this commit deprecate or contradict an existing entry? Update or remove the stale one.

This catches the "no tag since last update" case where tag-based range (`vX.Y..HEAD`) is unavailable.

### Step 4: Draft the changelog entries

Each entry follows this format:

```markdown
- **Feature or component name** — one-line description of what changed, ending
  with a useful detail. GitHub issue/PR reference in parens if available
  (#12345)
```

Rules:
- **One bullet per logical change.** Don't merge multiple fixes into one bullet.
- **Component prefix in bold:** **Desktop: **, **TUI: **, **Gateway: **, **CLI: **, **Kanban: **, **Dashboard: **
- **Include PR/commit references** in parens at the end: `(#40235)` or `(#9c1bb8d2c)`
- **Wrap long bullets** at 80 chars with 2-space indent continuation
- **Keep descriptions user-facing** — describe the observable effect, not internal internals

### Step 5: Apply the patch

If the `[Unreleased]` section was actually released:

1. Rename `[Unreleased]` → `[vYYYY.M.D] — YYYY-MM-DD`
2. Add a fresh `## [Unreleased]` section before it
3. Populate the new `[Unreleased]` section with commits since the tag

Use `patch()` for the edit.

### Step 6: Commit

```bash
git add CHANGELOG.md
git commit -m "docs(changelog): tag vYYYY.M.D as released, add Unreleased section for post-release commits"
```

## Version Convention

Hermes uses **date-based version tags** (`vYYYY.M.D`), not SemVer:

```
v2026.6.5     → Released 2026-06-05
v2026.5.29.2 → Released 2026-05-29 (patch 2)
```

The CHANGELOG header links these tags to their release dates. The `[Unreleased]` section is always at the top of the file, before all released versions.

When a version is released:
1. Remove "— Unreleased" from its section header
2. Append "— YYYY-MM-DD" (the tag date)
3. Create a fresh `## [Unreleased]` section above it
4. Add a `---` separator between Unreleased and the oldest released section

## Upstream Release Tracking (Hermes Config Repo Pattern)

When the repository is a **config overlay** (like hermes-config), not the upstream project itself, the CHANGELOG only tracks config-repo changes. Upstream Hermes Agent releases need a separate document (`docs/HERMES_RELEASE_NOTES.md`) to track what changed and what it means for the local config.

### Workflow

1. **Detect new releases** — Check upstream git tags since the last pulse:
   ```bash
   cd ~/AppData/Local/hermes/hermes-agent && git tag -l 'v*' --sort=-v:refname | head -10
   ```

2. **Summarize changes** — Extract features by release range. Read the tag annotation for the major release theme, then list commits:
   ```bash
   # Feature commits since a specific tag
   git log PREVIOUS..LATEST --oneline --no-merges --format="- %s" | grep -E "^\- (feat|fix)" | sort

   # Tag annotation for major theme
   git cat-file -p LATEST | head -20
   ```

3. **Organize by subsystem** — Group features into user-facing subsystems (PTY Sessions, MCP, Desktop, CLI, Dashboard, Auth, Discord, WhatsApp, Session Export, Delegation, Cron, etc.), not git-log directory prefixes. One bullet per change with **component prefix in bold** and upstream PR references: `(#60507)`.

4. **Include upgrade guidance** — Add an "Upgrading" section with new config keys, post-upgrade actions (gateway restart, config migration), and a link to upstream GitHub Releases.

5. **Cross-reference from root README** — Add `docs/` to the structure table and a Quick Start link to the release notes.

### When to Update

- During the first docs-lead pulse after an upstream release tag appears
- When `pip show hermes-agent` version is behind the latest git tag
- As part of the regular pulse cycle (every 1-3 days)

### Don't

- Don't add upstream changes to the config-repo CHANGELOG (it tracks config changes only)
- Don't duplicate content already in GitHub Releases — link to them
- Don't omit the `pip install --upgrade hermes-agent` command in the Upgrading section

## Digest Append (Safe-Content Pattern)

When delivering pulse findings via a shell script that interprets the message as arguments, special characters (`(`, `)`, `[`, `]`, `` ` ``, `#`, `-`, `!`, `&`, `|`) cause bash word-splitting and syntax errors.

**Problem:** `append-digest.py` reads the message as shell arguments:
```bash
# These fail because bash interprets (), #, etc.
python append-digest.py "Scribe Pulse" "- **Feature** (#12345) — description"
```

**Workarounds (in priority order):**

1. **Single-quote the outer string** and escape any single quotes:
   ```bash
   python append-digest.py 'Scribe Pulse' '- Added: /version command (CLI/gateway/TUI/desktop)'
   ```

2. **Use a temp file then pass via `cat`**: safest for multi-line content:
   ```bash
   printf '%s\n' '- Added: /version command' > /tmp/digest.txt
   printf '%s\n' '- Fixed: IME composition for CJK' >> /tmp/digest.txt
   python append-digest.py "Scribe Pulse" "$(cat /tmp/digest.txt)"
   ```

3. **Use a heredoc** for multi-line content:
   ```bash
   python append-digest.py "Scribe Pulse" "$(cat <<'EOM'
   - Added: /version command (CLI/gateway/TUI/desktop)
   - Fixed: desktop IME composition for CJK input
   EOM
   )"
   ```

**Best practice for cron pulses:** Write findings to a temporary markdown file first, then pass via `$(cat /tmp/file)` read. This avoids shell interpretation entirely.

## Common Pitfalls

1. **The "Unreleased" section was actually released.** Check `git tag -l 'v*'` — if a tag exists for the version in the CHANGELOG header, it's released. Rename immediately.

2. **Missing commits because `since` date was too recent.** Always use tag-based range (`vX.Y..HEAD`) rather than a date-based filter. Tags are precise; dates miss commits before your cutoff.

3. **Categorizing a mixed-type commit incorrectly.** A commit may say `fix: add X` — look at the *actual change*, not just the prefix. New features go in Added even if the prefix says `fix`.

4. **Shell-mangling digest content.** See "Digest Append" section above. Always test the shell command locally or use a temp file approach.

5. **Forgetting to commit the CHANGELOG change.** The changelog is versioned — if you don't commit it, the next pulse finds the same stale data.

6. **Section header mismatch.** The CHANGELOG header must match the actual tag name exactly. Use `git tag -l` to verify.

7. **Duplicate entries between Unreleased and released sections.** When moving content from Unreleased to a released section, make sure every entry moves — none get left behind.

8. **Missing PR/commit references.** Always include `(#NNNNN)` or `(#shortsha)` — these are crucial for readers tracing back to the source.

9. **Duplicate section headers from multiple edits.** When multiple people edit the CHANGELOG across different sessions, `### Changed` (or any other section header) can accumulate as duplicate blocks. Always scan for duplicate headers and merge them. Keep a Changelog format allows multiple `### Added`/`### Changed`/`### Fixed` blocks in a section, but merging them into one block per category is cleaner and easier to read.

10. **No release tag since last CHANGELOG update.** When the repo has no new tag (common for config overlays or slow-moving projects), tag-based range (`vX.Y..HEAD`) returns nothing useful. Use `git log --oneline --after=<date-of-last-changelog-entry>` instead, then cross-reference each commit against existing `[Unreleased]` entries to find undocumented changes.

## Verification Checklist

- [ ] Latest tag matches a CHANGELOG section header exactly
- [ ] `git log <latest-tag>..HEAD` output all accounted for in `[Unreleased]`
- [ ] No "Unreleased" sections that were actually released
- [ ] Each entry in the correct category (Added/Changed/Fixed/Removed)
- [ ] GitHub PR/issue numbers present where available
- [ ] `git add CHANGELOG.md && git commit -m "docs(changelog): ..."` done
- [ ] All special characters in digest/delivery content escaped or piped safely
- [ ] No duplicate section headers (e.g., multiple `### Changed` or `### Added` blocks) exist in the modified section
- [ ] CHANGELOG retains the initial `---` separator between Unreleased and the first released section (if any released sections exist)
