---
name: scaffold
description: Set up or align a non-code ops/PM repo with the ops folder structure, CLAUDE.md, and INDEX.md hierarchy.
disable-model-invocation: true
---

# Ops Scaffold

Set up a new non-code project management repo, or adjust an existing one to match the ops conventions.

## Detect Mode

Check the current directory:

- **If `CLAUDE.md` exists** → **Adjust mode**: read it, compare against the template below, and propose specific changes. Don't overwrite — use Edit to patch. Ask before creating missing folders.
- **If no `CLAUDE.md`** → **New repo mode**: run the full interview and scaffold from scratch.

## Interview (New Repo Mode)

Ask the user:

1. **Project name** — what the project is called
2. **One-paragraph description** — what the project does, who it's for
3. **Constraints** — team size, budget, timeline, key limitations
4. **The charter** — one topic at a time, offering your best guess from what they've said, and reading each answer back before you write it: who the project is for and the job they need done; 2-4 goals for the near term, each with how they'd know it is working; the audiences those goals target beyond the people it's for (a funder, a partner, a would-be maintainer); non-goals; what they care about and won't trade away; how bold to be. These become `charter.md`
5. **Initial domain areas** — what topics will the project cover? These become the initial subfolders. Examples:
   - Marketing, legal, fundraising, partnerships, technical research
   - Or more specific: grants, audience growth, competitor analysis
6. **Connected to a coding repo?** — ask if this ops repo is paired with a codebase. If yes, ask for the relative path from this repo to the code repo root (e.g., `../` if sibling directories, `../app/` if nested). This enables read-only access to the code for context.

## Interview (Adjust Mode)

Read the existing structure (CLAUDE.md, MEMORY.md, folder listing). Then ask:

1. **What needs changing?** — or just check against the template and propose fixes
2. **Missing folders?** — offer to create any missing standard folders with INDEX.md files
3. **CLAUDE.md drift?** — show specific differences from the template and offer to patch. An `## Autopilot` section, which autopilot's setup writes, is not drift: leave it as it is. An `autopilot/` folder is autopilot's memory from before it moved into this layout: leave it, and suggest running autopilot in a session started from the code repo, which moves it
4. **No `charter.md`?** — a repo set up before it existed keeps its goals in MEMORY.md, under "Constraints & Goals". Offer to move them into a new `charter.md` (template below), asking for what the template needs and MEMORY.md doesn't say, and to leave the constraints in MEMORY.md with the pointer line from its template. Where an `autopilot/` folder exists, leave this to autopilot's move, which merges its own charter in

## Directory Structure

```
<project-dir>/
├── .claude/
│   └── settings.json
├── state/
│   └── INDEX.md
├── backlog/
│   └── INDEX.md
├── references/
│   └── INDEX.md
├── artifacts/
│   └── INDEX.md
├── plans/
│   ├── INDEX.md
│   └── completed/
│       └── INDEX.md
├── .update/
│   └── .gitkeep
├── .gitignore
├── CLAUDE.md
├── MEMORY.md
└── charter.md
```

For each domain area the user specified, create a subfolder with an `INDEX.md` in the appropriate parent:
- Research topics → subfolders under `references/`
- Task areas → subfolders under `backlog/`
- Only create `state/` subfolders if the user has multiple distinct state areas

Example: if the user says "grants, marketing, legal" →
- `references/grants/INDEX.md`
- `references/marketing/INDEX.md`
- `references/legal/INDEX.md`
- `backlog/grants/INDEX.md` (if grants involve actionable tasks)

## .claude/settings.json

Read the template from `settings-json-template.md` (in this skill's directory). It covers both `.claude/settings.json` (enables ops plugin, base permissions) and `.claude/settings.local.json` (disables coding plugins).

## Connected Coding Repo (if applicable)

If the user said this ops repo is connected to a coding repo, set up read-only access:

### 1. Create `.claude/settings.local.json`

```json
{
  "permissions": {
    "allow": [
      "Read(<relative-path>/**)"
    ],
    "deny": [
      "Write(<relative-path>/**)",
      "Edit(<relative-path>/**)"
    ]
  }
}
```

Replace `<relative-path>` with the path the user provided (e.g., `../`, `../app`).

### 2. Add to CLAUDE.md

Add a section after "Working Directory":

```markdown
## Connected Codebase

This ops repo is paired with a coding repo at `<relative-path>`. You have **read-only** access to it for context — understanding architecture, reading implementations, checking current state.

**You MUST NEVER write, edit, or create files in the connected codebase.** All outputs belong in this PM folder. If work needs to happen in the code repo, produce a spec or brief in `artifacts/` that the user takes there.

**When to read the codebase:**
- To ground research or strategy in the actual implementation
- To verify state file accuracy against current code
- To inform specs and briefs with real architecture details
- When backlog items reference code features or components

**How to reference code:**
- Use relative paths: `<relative-path>/src/components/Header.tsx`
- Cite specific files and line numbers when referencing implementation details in artifacts
```

### 3. Add to MEMORY.md

Under the project description, add:

```markdown
## Connected Codebase

Paired with coding repo at `<relative-path>`. Read-only access for context. Never edit code — produce specs/briefs in artifacts/ instead.
```

## .gitattributes

Normalize line endings to LF across all platforms:

```
* text=auto eol=lf
```

## .gitignore

```gitignore
# AI development
.playwright-mcp/
.claude/settings.local.json
.claude/worktrees/
CLAUDE.local.md
nul
NUL

# IDE
.vscode/

# Update inbox (keep the directory, ignore contents)
.update/*
!.update/.gitkeep
```

## MEMORY.md

**MEMORY.md is for stable project context only** — description, constraints, and key learnings, with a pointer to `charter.md` for the goals. It is NOT for task status, WAITING markers, blocked items, or anything that changes week-to-week. Those belong in `state/` and `backlog/` files.

Fill in from the interview answers:

```markdown
# Project Context

_Last updated: <today's date>_

## The Project

<one-paragraph description from interview>

Goals, who the project is for and what it won't do: `charter.md`.

## Constraints

<constraints from interview, as bullet points>

## Key Learnings

_None yet._
```

## charter.md

**The charter is the one place the project's goals live**, every kind of goal: what the project delivers, and also who should run it, how it is funded, who hears about it. Every finder, `/ops:prioritize` and `/ops:whats-next` measure work against it. It changes only when the user says a goal changed.

Fill in from the interview's charter answers:

```markdown
# Charter — <project name>

_Last updated: <today's date>_
Confirmed: <today's date>

## Who it's for
<the primary group, in one or two sentences; secondary groups marked as such>

## The job they need done
<what they are trying to get done, in their words>

## Goals
1. <outcome, said as something that could be observed> — how we'd know: <signal>
2. …

## Audiences
- <each group a goal targets beyond the people it's for, and which goal: a funder, a partner, a would-be maintainer>

## Non-goals
- <what this project deliberately does not do, and why>

## What the owner cares about
- <taste, principles, things they won't trade away>

## Risk appetite
<how bold to be: what is live or public, who is hurt by a bad change>
```

Goals are numbered because other files refer to them by number. `Confirmed:` is the date the user last read the whole charter back and agreed with it.

## CLAUDE.md

Read the template from `claude-md-template.md` (in this skill's directory). Write it as the repo's CLAUDE.md, customizing `[PROJECT NAME]` and adjusting the Working Directory section if the repo is nested inside a code repo.

**Important:** The template's instructions (state vs. backlog separation, INDEX.md content standards, folder structure rules, etc.) also govern the scaffolding itself. When creating initial files — especially if the user provides content to ingest — follow these conventions from the start. Don't just write the rules into CLAUDE.md and then violate them in the same scaffolding pass.

## INDEX.md Files

Each INDEX.md should have real content, not placeholder comments. Write a brief overview of what that folder will contain based on the interview context.

**Root-level folders** (state/, backlog/, references/, artifacts/):

```markdown
# <Folder Name>

<One sentence describing what this folder contains in the context of this specific project.>

## Contents

_No files yet._
```

**Subfolders** (e.g., references/grants/):

```markdown
# <Topic>

<One sentence describing what research/tasks this subfolder covers.>

## Contents

_No files yet._
```

**plans/completed/INDEX.md:**

```markdown
# Completed Plans

Archived plans with documented outcomes.

## Contents

_No completed plans yet._
```

**plans/INDEX.md:**

```markdown
# Plans

Active plans. Don't update this INDEX for active plans — just create plan files here and move them to `completed/` when done.
```

## Initial State Files

If the user provided enough context during the interview, create 1-2 initial state files documenting what's already known:

- `state/platform.md` — if there's an existing product/service to document
- `state/audience.md` — if there are existing users/subscribers
- `state/<domain>.md` — for any area where current facts are known

Update `state/INDEX.md` to list these files.

## Initial Backlog Items

Ask the user: "What are the first 3-5 things you want to work on?" Add these to the appropriate backlog file(s), ordered by priority.

## Git Init (New Repo Mode)

Before creating any files, run `git init` in the project directory, then `git branch -M main` to rename the default branch. Create the `.gitattributes` file immediately after init (before other files) so all tracked files get normalized. The finalized scaffolding becomes the first commit.

## README.md

Write a project README covering:

1. **Header**: Project name and one-paragraph description from the interview.
2. **Prerequisites**: Mention that this repo is designed to work with [Claude Code](https://claude.com/claude-code) and the **ops** plugin.
3. **Key Commands**: The ops-relevant commands — interactive (`/ops:handle`, `/ops:whats-next`, `/ops:update`, `/ops:tidy`), discovery (`/ops:find-tasks`, `/ops:find-opps`, `/ops:find-all`), and autonomous (`/ops:get-to-work`, `/ops:batch-plan`, `/ops:batch-execute`, `/ops:review-followup`).
4. **Folder Structure**: This repo's specific folders with one-line descriptions based on the interview context.
5. **Typical Workflow**: 4-5 example commands using project-relevant language.

## Verification

After scaffolding (new repo) or adjusting:

1. Verify every folder has an INDEX.md (skip an `autopilot/` folder from before autopilot moved into this layout: autopilot moves it)
2. Verify `charter.md` exists with its goals, and MEMORY.md's references are valid
3. Verify CLAUDE.md has no remaining `[PROJECT NAME]` placeholders
4. Run `ls` on each directory to confirm structure matches expectations
5. Commit only the files this run wrote or changed, by explicit pathspec: `git add -- <paths>`, then `git commit -m "<message>" -- <paths>`, leaving out the gitignored `.claude/settings.local.json`. In new repo mode that is every file scaffolded, as the initial commit `"Initial scaffolding"`; in adjust mode, a message saying what was aligned. Never `git add -A`, `git add .` or a bare `git commit`: in an existing repo they sweep another writer's work into the commit.
