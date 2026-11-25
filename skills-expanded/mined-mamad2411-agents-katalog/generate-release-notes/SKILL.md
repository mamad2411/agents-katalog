---
name: generate-release-notes
description: This skill should be used when the user asks to "generate release notes", "generate changelog", "create release notes", "write changelog", "what changed since last release", "prepare release notes", "update changelog", or "summarize changes from git history". Parses conventional commit messages to produce categorized, well-formatted release notes or changelog entries.
---

# Release Notes Generator

Generate release notes and changelogs by parsing conventional commit messages from git log history. Commits following the Conventional Commits specification (feat:, fix:, docs:, etc.) are categorized, grouped, and formatted into professional markdown output.

## Workflow

### Step 1: Determine Output Type

Ask the user what they need:

- **Release Notes** — a single release summary written to `RELEASE_NOTES.md`
- **Changelog** — append to an existing `CHANGELOG.md` (or create one)
- **Both** — generate both files

### Step 2: Determine Commit Range

Identify which commits to include. Two approaches:

**Since last tag (default):**
The parser script automatically detects the latest tag and uses `<tag>..HEAD` when no range is provided. To confirm the range with the user before generating, run `git describe --tags --abbrev=0` to display the latest tag.

**Custom range:**
Accept a user-specified range like `v1.0.0..v2.0.0` or `v1.0.0..HEAD` and pass it as the first argument to the parser script.

If no tags exist, ask the user for a range or default to all commits (the script handles this automatically).

### Step 3: Parse Commits

Run the parser script to extract structured commit data. The `${CLAUDE_PLUGIN_ROOT}` variable is set automatically by Claude Code when the plugin is installed:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/generate-release-notes/scripts/parse-commits.sh [<range>]
```

The script outputs one block per commit with fields: `COMMIT`, `TYPE`, `SCOPE`, `BREAKING`, `DESCRIPTION`, `BODY`, `FOOTERS`.

### Step 4: Categorize and Format

Group parsed commits by type into sections using this mapping:

| Type | Section Heading |
|------|----------------|
| feat | Features |
| fix | Bug Fixes |
| perf | Performance Improvements |
| refactor | Code Refactoring |
| docs | Documentation |
| style | Styles |
| test | Tests |
| build | Build System |
| ci | Continuous Integration |
| chore | Chores |
| revert | Reverts |

**Ordering:** List sections in the order shown above. Within each section, list entries alphabetically by scope (ungrouped entries last).

**Breaking changes:** Collect all commits with `BREAKING:yes` into a dedicated "BREAKING CHANGES" section at the top, regardless of their type. These also appear in their normal type section.

**Scope grouping:** When multiple commits share a scope, group them under a bold scope label.

**Commits with type "other":** Collect into an "Other Changes" section at the bottom. These are commits that do not follow the conventional commit format.

### Step 5: Determine Version

If the user provides a version number, use it. Otherwise, suggest a version based on SemVer rules:

- Any `BREAKING:yes` commit → suggest MAJOR bump
- Any `feat` commit → suggest MINOR bump
- Only `fix`, `docs`, `style`, etc. → suggest PATCH bump

Read the latest tag to determine the current version and calculate the next version. Present the suggestion and let the user confirm or override.

### Step 6: Write Output

**Release Notes** → Write to `RELEASE_NOTES.md` (overwrite previous content).

**Changelog** → Prepend new version entry to `CHANGELOG.md`. If the file does not exist, create it with a header. Preserve all existing entries below the new one.

Consult `references/formats.md` for the exact output templates.

### Step 7: Summary

After writing, display:
- Version number used
- Number of commits processed
- Breakdown by category (e.g., "3 features, 2 bug fixes, 1 breaking change")
- File(s) written

## Handling Edge Cases

**No conventional commits found:** Warn the user that no parseable commits were found. Offer to list raw commit messages instead.

**Mixed conventional and non-conventional:** Process conventional commits normally, list non-conventional commits under "Other Changes."

**Empty range:** If the range produces no commits, inform the user and suggest checking the range.

**Monorepo with scopes:** When scopes map to packages/modules, offer to group by scope as top-level sections instead of by type.

## Additional Resources

### Reference Files

For detailed output format templates and examples, consult:
- **`references/formats.md`** — Complete output templates for release notes and changelog, with examples of each section type

### Scripts

- **`scripts/parse-commits.sh`** — Parses git log into structured commit data. Accepts an optional range argument. Handles conventional commit parsing, scope extraction, breaking change detection, and footer parsing.
