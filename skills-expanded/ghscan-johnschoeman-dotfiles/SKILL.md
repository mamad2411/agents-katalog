---
name: emerge
description: Scan recent internal writing for recurring themes coalescing into something bigger. Surfaces patterns ready to become formal projects. Use for periodic review, before planning sessions, or when asking "what keeps coming up?"
---

# Emerge — Surface Patterns from Internal Writing

Read-only skill. Scans recent weekly notes, daily notes, and domain files for recurring themes, cross-references against existing projects, and surfaces clusters ready to become formal projects. Never modifies files.

## Process

### 1. Gather Weekly Notes

Read all non-archived `_daily/wk_*.md` files (exclude `wk_template.md`). These are the primary source — typically 5-8 recent weeks.

From each weekly note, extract:
- **`# Narrative`** — richest source of recurring themes
- **`# Reflections and Concerns`** — HMW questions that repeat across weeks = strong signal
- **`## Red Flags`** — persistent flags = unaddressed need
- **`# Notes`** — raw observations
- **`## Next Week Intentions`** — what keeps getting re-prioritized

### 2. Gather Supporting Sources

Skim these for additional signal (don't read exhaustively):

- **Unarchived daily notes** (`_daily/dn_*.md`) — `# Notes` sections
- **Domain research notes** (`*/_research-notes.md`) — accumulated knowledge
- **Processed content notes** (`_content-notes/_processed/`) — external ideas

### 3. Extract and Cluster Themes

**Extract:** From each weekly note, list distinct themes, concerns, and topics. Tag each with the week it appeared in.

**Cluster:** Group related observations across weeks. Look for:
- Same keywords or phrases in multiple weeks
- Conceptual similarity (e.g., "therapy", "therapist", "self-reflection" cluster together)
- Same life domain getting repeated attention
- HMW questions that echo each other
- Red flags that persist without resolution

**Rank clusters by:**
1. **Recurrence** — how many weeks? (3+ = strong)
2. **Recency** — still showing up in latest 1-2 weeks?
3. **Intensity** — how much was written? (full paragraphs vs. brief mentions)

### 4. Cross-Reference Existing Projects

Read `_plans/projects/*.md` frontmatter (skip `_project_template.md`). Extract `status` and project name.

For each theme cluster, check:
- **Already tracked** — maps to a `now` or `next` project → note it
- **Partially tracked** — `later` status but theme keeps recurring → suggest promoting
- **Untracked** — no project covers it → candidate for new project

### 5. Assess Readiness

Categorize each untracked or partially tracked cluster:
- **Ready to emerge**: 3+ weeks, clear actionable direction, no active project
- **Emerging**: 2+ weeks, direction forming but not yet clear
- **Just surfacing**: 1-2 mentions, worth watching

### 6. Output Report

Use the [output format and guidelines in REFERENCE.md](REFERENCE.md).

## Vault Path

This is a global skill. The vault is at the root of the `notes` repository. Weekly notes at `_daily/wk_*.md`, daily notes at `_daily/dn_*.md`, projects at `_plans/projects/*.md`.

If `.claude/docs/planning.md` exists in the current repo, use it for additional context.
