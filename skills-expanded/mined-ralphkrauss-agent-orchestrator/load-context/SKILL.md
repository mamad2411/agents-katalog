---
name: load-context
description: Load existing context files into the conversation for a feature branch. Use when user says "load context", "read context", "get context", or wants to resume work on a branch where /build-context was already run.
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Load Context

Load pre-built context files into the current conversation so you can immediately proceed with planning or implementation — no research phase needed.

**This is the complement to `/build-context`.** Use `/build-context` to create context files. Use `/load-context` to reload them in a new conversation. Use `/update-context` to update stale project context without re-extracting API docs.

## Instructions

### Step 1: Detect Branch and Find Context Files

1. Get the current git branch: `git branch --show-current`
2. Glob for context files: `contexts/{branch-name}/**/*.md`
3. If no context files found:
   - Tell the user: "No context files found for branch `{branch-name}`. Run `/build-context` first."
   - Stop here.

### Step 2: Read Context Files (tier-aware)

Read files in this order for optimal context placement:

1. **`context.md`** (Tier 3 — combined summary) — read first for orientation
2. **`api-context.md`** (Tier 1 — cached API reference) — read second for provider knowledge
3. **`project-context.md`** (Tier 2 — dynamic project state) — read third for current state

If the tiered files don't exist (legacy single-file format), read whatever `.md` files are present.

### Step 3: Check Freshness

Parse the YAML front matter from each tier file:

- **api-context.md**: check `generated_at` — this is cached and rarely stale
- **project-context.md**: check `generated_at` — if older than 1 day, warn the user:
  ```
  ⚠ Project context was built on {date}. Plans, reviews, and code may have changed.
  Run `/update-context` to update it (~1 min) or `/build-context` for a full rebuild.
  ```

### Step 4: Read Must-Read Files

1. From the context files, find the **Must-Read Files** section
2. Extract file paths from **Critical** and **Important** tables (skip **Reference**)
3. Deduplicate across all context files
4. Verify each file exists (skip missing with a note)
5. Read all existing critical and important files using parallel agents if there are many files (>10)

### Step 5: Summary

```
Context loaded for branch `{branch-name}`.

Tiers:
  - API context: {generated_at} {(N days old)}
  - Project context: {generated_at} {(N days old)} {⚠ stale if > 1 day}

Context files read: {N}
Must-read files read: {N} critical, {N} important ({N} skipped — not found)

Critical path:
  1. {from context file}
  2. ...

Plan status:
  - Completed: {summary}
  - In progress: {summary}

Reference files available (not loaded): {N}

Ready for the next task.
```

## Critical Rules

- **Never modify context files** — this skill is read-only
- **Read in tier order** — context.md first (orientation), then api-context.md (reference), then project-context.md (current state)
- **Skip reference-priority files** — only read critical and important; mention reference files are available
- **Warn on stale project context** — if project-context.md is older than 1 day, suggest `/update-context`
- **Deduplicate across files** — if multiple files list the same must-read path, read it once
- **Fail fast if no context exists** — suggest `/build-context`

## Reference

- `.agents/skills/build-context/SKILL.md` — creates context files (tiered)
- `.agents/skills/update-context/SKILL.md` — lightweight update of project context
