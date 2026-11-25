---
name: study
description: Codebase research and exploration. Maps an area of the codebase and optionally relevant external sources, synthesizes findings into session context (no file output). Use before /plan when context is thin, or to understand an unfamiliar area.
---

# Study (Codebase Research)

Build session understanding of a codebase area. Read project context, dispatch parallel sub-agents, present a synthesized report. **No file artifact** — the value is the context loaded into this conversation.

Use when you want to learn how an area works, scope a vague topic, or prime context before `/plan`. Often invoked at the start of a fresh session or when `/plan` needs more background.

## Input

> $ARGUMENTS

If empty, ask what to study.

## Phase 1 — Project Context

Read first, before spawning agents:

1. **`CLAUDE.md`** at project root — architecture, conventions, stack.
2. **`.claude/rules/`** — project-specific constraints.
3. **`docs/`** if it exists — deeper architecture documentation.

Note where the topic likely lives (folders, modules, key types). Use `Glob` + `Grep` to locate entry points before spawning agents.

## Phase 2 — Parallel Exploration

Spawn 2-3 sub-agents in **parallel** (one message, multiple `Agent` calls) using `model: "sonnet"` per `wf-agents-on-sonnet.md`. Each agent gets a focused, self-contained brief.

**Always:**

- **Codebase agent** — trace the topic across files. Identify entry points, data flow, key abstractions, tests. Returns a structured note.

**Conditionally** (decide from the topic):

- **Sub-area agent** — when the topic spans 2+ distinct sub-areas, split the codebase scan into parallel focused passes (e.g. "model layer" vs "rendering" vs "interaction").
- **External research agent** — when the topic involves third-party libraries, framework versions, or domain knowledge not derivable from the code, use `WebSearch` / `WebFetch` on official docs. Cross-check ≥ 2 sources. Skip for purely-internal topics.

Each agent returns: `## Findings`, `## Open questions`, `## Cited paths/sources`. Cap each agent's report at ~400 words.

## Phase 3 — Synthesize

Pull agent reports together. Present in the session:

- **Lay of the land** — 3-5 bullet summary of the area.
- **Key files / types** — paths with one-line descriptions.
- **Data flow** — how the topic threads through the code.
- **Open questions** — things unclear from code alone, worth confirming with the user.
- **External notes** (if external agent ran) — version-specific facts, gotchas, references.

Keep it tight. Synthesis, not transcript. The reader is the next turn of this conversation (or `/plan`).

## What this skill does NOT do

- No file output. No `plans/research/*.md` or similar.
- No task list, no planning. Use `/plan` after for that.
- No code changes. No commits.

## When to skip

- Topic fully covered by current session context.
- Single-file lookup — use `Read` / `Grep` directly.
- The user wants a plan now — go straight to `/plan` (it invokes `/study` when its Phase 1 detects thin context).
