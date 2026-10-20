---
name: gh-release-notes-writer
description: Use when the user says "cut a release", "release notes", "tag a new version", "publish a release", "prepare a release". NOT for opening pull requests — that is gh-pr-create.
---

# Release Notes Writer

GitHub Releases (`gh release`). Origin is out of scope for this plugin; use
this `gh-release-notes-writer` skill on GitHub only.

## Execution Backend

1. Verify `git` with `git --version` and `gh` with `gh auth status`.
2. Run the bundled scripts and plain `git`/`gh` workflow below.
3. If either verification fails, STOP and report the failed check. For a `gh`
   failure, report verbatim: "`gh` is missing or unauthenticated. Install it if
   needed, run `gh auth login`, then retry."

Generate professional release notes by scanning git history, then create and publish GitHub releases.

## Versioning Scheme

Supported formats:
- `vMAJOR.MINOR`
- `vMAJOR.MINOR.PATCH`

Default selection:
- Start with `vMAJOR.MINOR`.
- If existing repo tags already use patch-level versions, continue with `vMAJOR.MINOR.PATCH`.
- Only move to patch-level tagging when the repo already follows it or the user explicitly requests it.
- Deterministic override: pass `--tag-scheme major|minor|patch` (or set `RELEASE_TAG_SCHEME`) to force the scheme.
- Convenience override: pass `--prefer-patch-level` to prefer `patch` when no explicit scheme is set.

Decision function used by `scripts/gather_changes.sh`:
- `determine_tag_scheme(base_tag, explicit_scheme, prefer_patch_level)` returns `explicit_scheme` first.
- If no explicit scheme is set, it infers from existing tags (`vX.Y.Z` -> `patch`, otherwise `minor`).
- If no prior tags exist, it still returns deterministically: `patch` when explicitly requested (or when `--prefer-patch-level` is set), otherwise `minor`.

If the repo already uses `vMAJOR.MINOR` with MINOR in `{0,5}`, preserve that pattern unless the user asks to move to patch-level tags.

| Version | Meaning |
|---------|---------|
| vX.0 | Major milestone or breaking changes |
| vX.5 | Mid-cycle feature release (when using the 0/5 scheme) |
| vX.Y.Z | Patch-level releases (bug fixes, small improvements) |

Progression (0/5 scheme): v1.0 → v1.5 → v2.0 → v2.5 → ...
Progression (patch scheme): v1.0.0 → v1.0.1 → v1.1.0 → v2.0.0 → ...

## Workflow

### 1. Prerequisites Check

```bash
scripts/check_prerequisites.sh
```

Verifies: gh authenticated, git repo clean, on a branch.

### 2. Gather Release Context

```bash
scripts/gather_changes.sh [last-tag] [--tag-scheme major|minor|patch] [--prefer-patch-level]
```

Returns: commits since last tag, changed files, suggested next version.
> Note: `gather_changes.sh` uses read-only `git` commands — no bot identity needed.

If no previous tags exist, gathers all commits and uses the flag/option to control first suggested version: `v1.0` for `major|minor`, `v1.0.0` for `patch`.

### 3. Generate Release Notes

Analyze the gathered changes and write notes following this structure:

```markdown
## What's New

[2-3 sentence thematic summary]

### ✨ Features
- Feature descriptions (user-facing impact)

### 🔧 Improvements  
- Enhancement descriptions

### 🐛 Bug Fixes
- Fix descriptions (if applicable)

### ⚠️ Breaking Changes
- Breaking change descriptions (major releases only)

---
**Full Changelog**: <previous-tag>...<new-tag>
```

Guidelines:
- Lead with user impact, not implementation details
- Group related changes
- Omit empty sections
- Use present tense ("Adds..." not "Added...")

### 4. User Confirmation

Before any git operations, present:
1. Proposed version number
2. Draft release notes
3. Request explicit approval

### 5. Create Release

```bash
scripts/create_release.sh <version> <notes-file>
```

Creates annotated tag (via `git`), pushes to remote (via `git push`), publishes GitHub release (via `gh`).


## Gotchas

1. **Tag already exists → must NOT silently reuse it** -- if the suggested version tag exists, surface an explicit error and suggest the next available version; never silently overwrite an existing release tag (it would rewrite GitHub release history).
2. **Uncommitted changes produce misleading release notes** -- always verify a clean working tree before gathering changes. `gather_changes.sh` runs `check_prerequisites.sh` first; if it is bypassed, dirty state bleeds into the release diff.
3. **User confirmation is mandatory before any git tag operation** -- always present the draft version + notes and wait for explicit approval. Auto-tagging without confirmation has caused accidental public releases on repos with branch protection that allows bot pushes.
4. **Route tag creation through `create_release.sh`** -- it creates the annotated tag, pushes it, and publishes the GitHub release in one verified sequence with the correct tagger identity; ad-hoc `git tag` + `gh release create` calls drift out of sync (tag pushed without release, or release against an unpushed tag).

## Error Recovery

| Error | Resolution |
|-------|------------|
| Tag exists | Suggest next available version |
| Uncommitted changes | List changes, suggest stashing or committing |
| gh not authenticated | Run `gh auth login` |
| Push rejected | Check branch protection, suggest PR workflow |
