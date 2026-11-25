---
name: weekly-status
description: "[DEPRECATED 2026-04-23] Use meetings/weekly/CLAUDE.md instead — its Step 5.0 covers the same mismatch-detection logic. This skill is kept for reference only."
alwaysApply: false
---

**DEPRECATED — Use `meetings/weekly/CLAUDE.md` (the Monday weekly prep skill) instead.**

The mismatch-detection logic that was this skill's unique value is now Step 5.0 of the weekly prep workflow. Invoking this skill separately creates redundant work and split gotchas. This folder is in `.claude/skills/_deprecated/` per STANDARDS.md; delete after one month of parallel availability.

Original instructions follow for reference only — do not run them.

---

# Weekly Status

Reads all roadmap/tracking sources, compares them, and produces a unified status report with mismatch flags.

## Trigger

"weekly status" or "pull status"

## Pre-Run

1. Read `.claude/skills/weekly-status/gotchas.md` (if it exists)
2. Read `roadmap/CLAUDE.md` for the list of tracking sources

## Execution

### Step 1: Read Sources
Pull current status from all tracking sources:
- Roadmap spreadsheet (if configured in `roadmap/CLAUDE.md`)
- Project tracker (Jira/Linear/GitHub Issues)
- Recent git log (last 7 days of commits in this repo)
- Project README.md files (for current phase/status)

### Step 2: Build Unified Table
For each active project, produce:

| Project | Phase (repo) | Status (tracker) | ETA | Owner | Last Updated | Flags |
|---------|-------------|-------------------|-----|-------|-------------|-------|

### Step 3: Flag Mismatches
- **Source disagreement:** Repo says "Coding" but tracker says "In Review"
- **Stale status:** Last updated > 2 weeks ago with no activity
- **Overdue ETA:** ETA has passed but project isn't marked complete
- **Missing tracking:** Project exists in repo but not in tracker (or vice versa)

### Step 4: Report
Present the table + flags. Ask if the user wants to:
- Fix any mismatches (update repo files or tracker)
- Add any missing projects
- Update any ETAs

## Post-Run

Append to `.claude/skills/weekly-status/runs.log`:
```
[date] | [projects checked] | [mismatches found] | [fixes applied]
```
