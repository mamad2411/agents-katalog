---
name: update-training
description: >-
  Audit training materials against Claude Code changelog and optionally fix
  issues. Uses parallel agents for scanning and fixing across 10 file groups.
---

# Update Training Materials Skill

Audit training materials against the official Claude Code changelog to find stale references,
missing feature coverage, and legacy content. Optionally fix all issues in parallel.

## Usage

```
/update-training                          # Scan only (audit report, no changes)
/update-training --fix                    # Scan and fix all issues
/update-training --fix --severity error   # Scan and fix only errors
/update-training --dry-run                # Show what would be fixed without applying
/update-training 2.0.0-2.1.37            # Audit only changes in version range
/update-training --focus docs             # Limit scan to docs/ only
/update-training --focus examples        # Limit scan to examples/ only
```

## Arguments

| Argument | Description |
|----------|-------------|
| `[version-range]` | Filter changelog to specific version range (e.g., `2.0.0-2.1.37`) |
| `--fix` | Apply fixes after scanning (without this, only reports findings) |
| `--severity <level>` | Filter fixes by minimum severity: `error`, `warning`, or `info` (default: all) |
| `--dry-run` | Show what would be fixed without writing any files |
| `--focus <area>` | Limit scan scope: `docs`, `examples`, or `all` (default: all) |

**Default behavior:** Scan only — display audit report without modifying files. `--fix` is required
to apply changes.

## Architecture

Three specialized agents work in phases:

| Agent | Purpose | Count |
|-------|---------|-------|
| **changelog-auditor** | Fetch and parse official changelog into structured JSON | 1 |
| **training-scanner** | Scan assigned file group against changelog data | 10 (parallel) |
| **training-fixer** | Apply targeted fixes based on scanner findings | 10 (parallel) |

## Orchestration Flow

```
/update-training [version-range] [--fix] [--severity <level>] [--dry-run] [--focus <area>]
       │
       ▼
  1. PARSE: Extract arguments and flags
       │
       ▼
  2. FETCH: Spawn 1x changelog-auditor agent
       │    - Fetches official CHANGELOG.md
       │    - Parses into structured JSON
       │    - Filters by version-range if specified
       │    - Output: {versions[], stale_patterns[], new_features[]}
       │
       ▼
  3. DISCOVER: Glob training files based on --focus flag
       │
       ▼
  4. GROUP: Split files into 10 groups by directory/topic proximity
       │
       ▼
  5. SCAN: Spawn 10x training-scanner agents IN PARALLEL
       │    - Input: assigned file group + parsed changelog
       │    - Output: JSON findings array per agent
       │
       ▼
  6. CONSOLIDATE: Merge and deduplicate all scanner findings
       │
       ├── No --fix → Exit with audit report
       │
       └── --fix →
       │
       ▼
  7. FILTER: Apply --severity filter to findings
       │
       ▼
  8. FIX: Spawn 10x training-fixer agents IN PARALLEL
       │    - If --dry-run: report what would change
       │    - Otherwise: apply targeted edits
       │
       ▼
  9. DISPLAY: Show fix summary with counts
```

## Instructions

### Step 1: Parse Arguments

Extract from the user's command:
- `version_range`: positional argument matching pattern `N.N.N-N.N.N` (or null for all versions)
- `fix_mode`: true if `--fix` is present
- `severity_filter`: value after `--severity` (or null to include all severities)
- `dry_run`: true if `--dry-run` is present
- `focus_area`: value after `--focus` (or `all`)

If `--dry-run` is present, implicitly enable `fix_mode` (dry run is a variant of fix).

### Step 2: Fetch and Parse Changelog

**Spawn 1 changelog-auditor agent.**

Use `subagent_type: "changelog-auditor"` with the Task tool.

**Agent Prompt:**

```
Audit the official Claude Code changelog.

Version range filter: {version_range or "all versions"}

Fetch the changelog from:
https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md

Parse ALL entries and return structured JSON with:
- versions[] - all version entries with their changes
- stale_patterns[] - outdated references with replacements
- new_features[] - significant new features for training coverage
- deprecations[] - deprecated features
- removals[] - removed features
- renames[] - renamed features/paths
- breaking_changes[] - breaking changes

Output the full JSON object as specified in your agent instructions.
```

Wait for the agent to complete. Extract the parsed changelog JSON from its response.

### Step 3: Discover Training Files

Use Glob to find training files based on the `focus_area`:

| Focus Area | Glob Patterns |
|------------|---------------|
| `all` (default) | `docs/*.md`, `examples/**/*.md` |
| `docs` | `docs/*.md` |
| `examples` | `examples/**/*.md` |

Collect all matching file paths.

### Step 4: Split Files into 10 Groups

Split discovered files into exactly 10 groups using directory/topic proximity:

**Grouping Algorithm:**

1. **Sort files by directory then filename** to cluster related files
2. **Group by directory first**: files in the same directory stay together
3. **Distribute evenly**: aim for roughly equal file counts per group
4. **Name each group** based on the primary directory/topic of its files

If fewer than 10 files exist, use fewer groups (one file per group minimum).

**Group Structure:**
```json
{
  "groups": [
    {
      "id": 1,
      "name": "core-docs-01-10",
      "files": ["docs/01-what-is-claude-code.md", "docs/02-installation.md", ...]
    },
    {
      "id": 2,
      "name": "core-docs-11-20",
      "files": ["docs/11-hooks.md", "docs/12-permissions.md", ...]
    }
  ]
}
```

### Step 5: Spawn Parallel Scanner Agents

**CRITICAL: Spawn all 10 scanner agents in a SINGLE message with 10 Task tool calls.**

Use `subagent_type: "training-scanner"` for each.

**Agent Prompt Template:**

```
Scan training materials in GROUP {N}: {group_name}

ASSIGNED FILES:
{list of file paths, one per line}

CHANGELOG DATA:
{full parsed changelog JSON from Step 2}

Scan each file for:
1. STALE references - outdated patterns from stale_patterns list
2. MISSING coverage - new features from new_features list not covered where relevant
3. LEGACY content - removed/deprecated features still presented as current

Output JSON with findings array as specified in your agent instructions.
```

Wait for ALL scanner agents to complete. Collect all responses.

### Step 6: Consolidate Scanner Results

After all scanner agents complete, merge and deduplicate findings:

1. **Collect**: Extract the JSON findings from each agent response
2. **Concatenate**: Merge all findings arrays into one
3. **Deduplicate**: Remove duplicates by (file, line, description) tuple, keeping highest severity
4. **Re-number**: Assign sequential IDs per type (STALE-001, STALE-002, etc.)
5. **Sort**: By severity (error > warning > info), then file path, then line number

**Track consolidation stats:**
- `raw_findings`: Total findings before dedup
- `after_dedup`: Final deduplicated count
- `dedup_rate`: Percentage reduction

### Step 7: Display Audit Report

Display the consolidated results:

```
Training Materials Audit Report
================================

Scan Summary:
  Files scanned: 45
  Groups: 10
  Scanner agents: 10

Consolidation:
  Raw findings: 80
  After dedup: 35 (56% dedup rate)

Summary:
  Total findings: 35
  Errors: 5
  Warnings: 20
  Info: 10

By Type:
  Stale references: 12
  Missing coverage: 15
  Legacy content: 8

Findings:
---------
[ERROR] STALE-001 (docs/02-installation.md:35)
  References ~/.claude.json which was moved to ~/.claude/settings.json
  Evidence: "Edit your `~/.claude.json` to configure..."
  Fix: Replace `~/.claude.json` with `~/.claude/settings.json`

[ERROR] LEGACY-001 (docs/10-settings.md:42)
  Shows 'claude config' command which was deprecated in v1.0.7
  Evidence: "Run `claude config set theme dark` to change..."
  Fix: Replace with direct settings.json editing instructions

[WARNING] MISSING-001 (docs/05-hooks.md)
  New hook event 'notification' not covered in hooks documentation
  Fix: Add section covering the notification hook event added in v2.1.0
...
```

**If `--fix` is NOT set:** Stop here. Display the report and exit.

**If `--fix` IS set:** Continue to Step 8.

### Step 8: Filter Findings by Severity

Apply the `--severity` filter:

| `--severity` Value | Include |
|---------------------|---------|
| `error` | Only severity = "error" |
| `warning` | severity = "error" OR "warning" |
| `info` or not set | ALL findings |

Group filtered findings by file, then reassign to the original 10 groups for parallel fixing.

### Step 9: Spawn Parallel Fixer Agents

**CRITICAL: Spawn all fixer agents in a SINGLE message with multiple Task tool calls.**

Only spawn fixer agents for groups that have findings after filtering. Use `subagent_type:
"training-fixer"` for each.

**Agent Prompt Template:**

```
Fix training material issues in GROUP {N}: {group_name}

DRY RUN: {true|false}

FINDINGS TO FIX:
{JSON array of findings for this group's files}

For each finding:
1. Read the file and verify the issue still exists
2. Apply the suggested fix with minimal changes
3. Record the result (applied or skipped with reason)

{If dry run: "DO NOT apply any changes. Only report what would be changed."}

Output JSON with fixes_applied and fixes_skipped arrays as specified in your agent instructions.
```

Wait for ALL fixer agents to complete. Collect all responses.

### Step 10: Display Fix Summary

```
Fix Summary
===========

{If dry run: "DRY RUN - No changes were applied"}

Applied ({count}):
  STALE-001: Replaced ~/.claude.json with ~/.claude/settings.json in docs/02-installation.md
  LEGACY-001: Updated 'claude config' to settings.json editing in docs/10-settings.md
  ...

Skipped ({count}):
  MISSING-001: No clear section to add notification hook coverage (docs/05-hooks.md)
  ...

Totals:
  Findings processed: 35
  Fixes applied: 28
  Fixes skipped: 7
```

## Error Handling

- If the changelog fetch fails, report the error and stop
- If any scanner agent fails, continue with results from others and note the failure
- If any fixer agent fails, continue with others and report failures
- If an agent returns invalid JSON, skip that agent's output and continue
- If grouping produces fewer than 10 groups (not enough files), use as many groups as there are files
- Always display partial results even if some agents fail
