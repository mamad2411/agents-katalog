---
name: review-context-hub
description: Review a repo as a context hub. Use when the user wants an overview of the repo structure, recent changes, standing instruction files, installed skills, remotes, or who has access.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# Review Context Hub

Review a repository as a context hub.

This skill is for understanding the **what** that lives in a repo:

- the outline of the repo
- recent changes
- standing instruction files
- installed skills
- git remotes
- who has access

Your job is not to make changes by default. Your job is to produce a useful orientation pass.

## When to Use

Activate this skill when the user asks to:

- review a context hub
- inspect a repo before doing work
- explain what context an AI would pick up from this repo
- show what instruction files or skills are present
- check remotes, ownership, or access

If the user is really asking for implementation, debugging, or code review, do not use this as the primary skill.

## Core Mental Model

- The context hub is about **what**
- Skills are about **how**

This skill reviews the **what**:

- what the repo contains
- what recent work happened
- what standing instructions exist
- what reusable skills are available
- what remotes and access boundaries exist

## Review Pass

Work from the repo root.

### 1. Outline the repo

Get a quick sense of the top-level structure.

Look for:

- main folders
- docs or notes areas
- workflow output folders
- instruction/config folders

Summarize the structure in plain language. Do not dump giant file listings unless the user asks.

### 2. Review recent changes

Inspect recent git history and current worktree state.

Look for:

- current branch
- uncommitted changes
- recent commits
- whether the repo looks actively used or stale

### 3. Review standing instruction files

Check for:

- `CLAUDE.md`
- `AGENTS.md`
- `GEMINI.md`
- nested variants if relevant

Explain what each one appears to govern.

### 4. Review installed skills

Check for skill directories such as:

- `.claude/skills/`
- `.agents/skills/` (shared by Codex and Gemini CLI)
- `.gemini/skills/`

Give a high-level overview:

- which skill systems are present
- what kinds of skills exist
- whether the repo appears to rely on local/project skills

You do not need to read every skill in full. Prefer names, descriptions, and obvious categories first.

### 5. Review remotes and ownership

Inspect git remotes.

Explain:

- where the repo is hosted
- whether it appears personal or organizational
- what that suggests about who owns the hub

### 6. Review access

If the GitHub CLI is available and authenticated, try to determine:

- whether the repo is public or private
- who the owner is
- who has collaborator/admin access, if that can be checked safely

If you cannot verify access directly, say so clearly and infer only from remotes, org ownership, and visibility.

## Output Format

Default to a short structured review:

### Context Hub Review
- **Repo outline:** ...
- **Recent changes:** ...
- **Instruction files:** ...
- **Skills present:** ...
- **Git remotes:** ...
- **Access/ownership:** ...
- **What this hub seems optimized for:** ...

Then add:

- **Gaps / risks**
- **Suggested next checks** if useful

## Good Behavior

- Be concise
- Prefer orientation over exhaustiveness
- Separate verified facts from inference
- Call out uncertainty clearly
- Do not assume GitHub access if you cannot verify it

## Useful Commands

See `reference/checklist.md` for a lightweight command checklist.
