---
name: session-start
description: Load persistent project memories from CogmemAi at the start of every session, so the assistant resumes with full context from prior conversations. Use as the very first action when a new session begins, when the user greets the assistant, when context has been compacted, or when switching projects. Calling this once at session start is the single most important continuity action.
metadata:
  author: HiFriendbot
  version: 1.0.0
  mcp-server: cogmemai
  category: developer-tools
  tags: [session, start, memory, mcp, context, onboarding, developer-tools]
---

# Session Start with CogmemAi

Run this skill at the start of every session, before responding to the user's first message. It loads the most important memories from prior sessions for the current project, so the assistant can pick up exactly where the last session left off.

## When to Use

- The very first turn of a new session, before any other action
- After any context compaction event (you'll see a summary of the prior conversation)
- When the user greets the assistant ("hi", "hey", "morning", "let's continue")
- When switching from one project to another within the same session
- When the user says "what were we working on?", "where did we leave off?", "remind me"

## How to Run

Call `get_project_context`. Optional but useful: pass a `context` parameter describing the current task, which biases the returned memories toward what's most relevant.

```
get_project_context({
  context: "implementing the new payments flow"
})
```

The response includes:

- Top memories ranked by importance and recency, scoped to the current project plus any global memories that apply
- A `health_score` (0-100) indicating overall memory quality
- Any pending tasks from prior sessions
- Active reminders set by the previous session via `set_reminder`

## What to Do With the Result

1. **Read every returned memory carefully.** They contain architecture decisions, preferences, gotchas, file paths, and bug fixes that took effort to discover. Treat them as authoritative for what was true when they were written.

2. **Verify before acting on memory-derived recommendations.** A memory that names a specific file, function, or flag is a claim about *the past*. If the user is about to act on your recommendation, confirm the artifact still exists. Things get renamed, removed, or never merged.

3. **Check pending tasks.** If `get_tasks` (or the embedded task list) shows in-progress or todo items, surface them to the user as "here's what was open" so the user can choose what to tackle.

4. **Honor active reminders.** If a reminder fires (e.g., "remember to delete the test data on the server"), surface it to the user immediately.

5. **Do not paraphrase memory contents back to the user as a long preamble.** The user doesn't need a recap. Use the memories silently to inform your work, and reference them only when relevant.

## Why This Matters

Without `get_project_context` at session start:

- The assistant re-asks questions the user already answered last session
- Decisions get re-litigated instead of executed
- File paths and architecture details get re-discovered, wasting time
- Open tasks get forgotten until the user remembers them
- The assistant feels like a stranger every session

With it:

- The assistant resumes with full prior context
- Multi-session work threads naturally
- The user feels continuity, not amnesia

## After Compaction

When Claude Code or any agent compacts your context mid-session (you'll see a summary of the prior conversation in your context window):

1. Call `get_project_context` immediately to reload memories
2. Pass the current task as the `context` parameter for relevance
3. Continue working, your memories bridge the gap

This recovery pattern is what turns a 200k-token conversation into one that can run indefinitely.

## Onboarding to a New Project

If `get_project_context` returns no memories (first session for this project):

1. Read the project's README, package.json, or equivalent
2. Use `ingest_document` to extract key facts from the documentation
3. Save 3-5 high-importance memories about the tech stack, architecture, and conventions
4. Save the user's stated preferences for this project as `preference` memories with `scope: "project"`

The next session will benefit from this groundwork via this same `get_project_context` call.

## Related Skills

- `cogmemai-memory` — full reference for memory management
- `save-context` — preserve in-flight work during a session
- `remember-this` — save explicit user instructions
- `search-before-debugging` — recall specific past fixes when a bug appears
