---
name: devel-jb-changelog
description: "` separator (line after intro paragraph), before the first existing version entry."
domain: cybersecurity
---

` separator (line after intro paragraph), before the first existing version entry. Do NOT replace the entire file — only insert the new entry block.

### Step 8: RELEASE_NOTES (Maintainer Only)

`specs/RELEASE_NOTES_<version>.md` is only generated when the user is the project maintainer (runkids). Contributors skip this step.

Check if running as maintainer:
```bash
git config user.name  # Should match maintainer identity
```

If maintainer:
- Read the most recent `specs/RELEASE_NOTES_*.md` as a style reference
- Generate `specs/RELEASE_NOTES_<version>.md` (no `v` prefix, e.g. `RELEASE_NOTES_0.17.6.md`)
- Structure:
  - Title: `# skillshare vX.Y.Z Release Notes`
  - TL;DR section with numbered highlights
  - One `##` section per feature/fix — describe **what changed** in plain language, with a CLI example or code block if relevant. No "The problem / Solution" structure — just state what it does now
  - Include migration guide if breaking changes exist

**RELEASE_NOTES wording rules** (same user-facing standard as CHANGELOG):
- Describe **what changed** from the user's perspective, not how the code changed
- **Never mention**: function names, variable names, struct fields, file paths, Go syntax, internal APIs
- ✅ Good: "Sync now auto-creates missing target directories and shows what it did"
- ❌ Bad: "upgraded `Server.mu` from `sync.Mutex` to `sync.RWMutex` and applied a snapshot pattern across 30 handlers"
- Keep it concise — a short paragraph per feature is enough, no need for multi-section breakdowns

If not maintainer:
- Skip RELEASE_NOTES generation
- Only update CHANGELOG.md + website changelog

## Rules

- **User perspective** — write for users, not developers
- **No fabricated links** — never invent URLs or references
- **Verify features exist** — grep source before claiming a feature was added
- **No internal noise** — exclude test-only, CI-only, or refactor-only changes
- **Conventional format** — follow existing CHANGELOG.md style exactly
- **Always sync both** — `CHANGELOG.md` and `website/src/pages/changelog.md` must have identical release entries
- **RELEASE_NOTES = maintainer only** — contributors only update CHANGELOG.md + website changelog
