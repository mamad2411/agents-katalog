---
name: recall
description: "Load the project context scaffold (.claude/context/) at session start or for a specific task."
disable-model-invocation: true
---

# Skill: Recall

Load the project **context scaffold** (`.claude/context/`) at the start of a session, or for a specific task.

> Scope: this skill loads the project context scaffold only. Cross-session *session memory* — the auto-memory `memory/MEMORY.md` index — is loaded automatically by the harness at session start, so `/recall` complements it rather than being the whole session-start story.

## When to Use

Run `/recall` at the beginning of a session, especially when:
- Starting work on a project you haven't touched recently
- Picking up a task that touches unfamiliar parts of the codebase
- Onboarding or context-switching between projects

Also useful mid-session: `/recall <task description>` to load context relevant to a specific task.

## Process

### Step 1: Check Scaffold Exists

Look for `.claude/context/ROUTER.md`.

**If it doesn't exist:** Check for `.claude/architecture.md` (monolithic fallback).
- If the monolithic file exists, read and summarize it. Suggest running `/intel` to generate the full scaffold.
- If neither exists, tell the user: *"No project context found. Run `/intel` to generate the context scaffold."*

**If it exists:** Continue to Step 2.

### Step 2: Read the Router

Read `.claude/context/ROUTER.md` to understand what context files are available.

### Step 3: Route by Arguments

**No arguments** → Overview mode:
1. List all context files with:
   - File name and purpose (from ROUTER.md)
   - Last updated date (from each file's header comment)
   - Line count (as a rough size indicator)
   - Status: "Populated" if the file has real content beyond the template, "Template" if still placeholder
2. Flag any files not updated in 30+ days as potentially stale
3. Print a one-line suggestion: *"Use `/recall <task>` to load context for a specific task, or `/intel` to refresh stale files."*

**With task description** → Targeted mode:
1. Match the task description against the Task Routing table in ROUTER.md
2. Read the matched context files (usually 2-3 files)
3. Print a concise summary of the loaded context:
   - Key architectural facts relevant to the task
   - Relevant conventions to follow
   - Relevant decisions that constrain the approach
   - Any patterns that apply
4. Keep the summary under 30 lines — the point is to prime context, not dump everything

### Matching Heuristics

When matching a task description to the routing table:

| Task Keywords | Routes To |
|--------------|-----------|
| "plan", "scope", "design", "architect" | Planning / Scoping |
| "add", "build", "create", "implement", "feature" | Adding a Feature |
| "fix", "bug", "debug", "error", "broken" | Debugging / Fixing |
| "review", "PR", "check", "audit" | Code Review |
| "onboard", "understand", "explain", "context" | Onboarding / Context |
| "refactor", "clean", "reorganize", "migrate" | Refactoring |

If the task description doesn't clearly match, default to Onboarding / Context (load everything).

## Output Format

**Overview mode:**
```
## Project Context Summary

| File | Last Updated | Lines | Status |
|------|-------------|-------|--------|
| architecture.md | 2026-03-15 | 45 | Populated |
| decisions.md | 2026-03-15 | 32 | Populated |
| conventions.md | 2026-03-10 | 28 | Populated |
| patterns/api-endpoints.md | 2026-03-12 | 35 | Populated |

⚠ conventions.md not updated in 20 days — consider running `/intel` to refresh.

Use `/recall <task>` to load context for a specific task.
```

**Targeted mode:**
```
## Context for: [task description]

**Architecture:** [1-2 key facts]
**Conventions:** [relevant rules]
**Decisions:** [relevant constraints]
**Patterns:** [applicable patterns, if any]
```

## Token Discipline

This skill is designed to be lightweight. Do NOT:
- Read every file in full and dump it into the conversation
- Include template placeholder content in summaries
- Read pattern files that aren't relevant to the task
- Summarize more than what's needed for the immediate task

The goal is to prime your context with the minimum needed to work effectively — not to replicate the scaffold in the conversation.
