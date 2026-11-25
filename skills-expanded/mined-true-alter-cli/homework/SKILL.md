---
name: homework
description: |
  State pre-flight for Claude Code before asking you anything that could be answered by reading current state. Stops CC from asking questions already answered by git, your MCP tools, your doc search, your doctrine/decision register, or the working tree.

  TRIGGER (manual): /homework, "do your homework", "check state first", "before you ask, look", "did you check".

  TRIGGER (automatic, CC self-fires): before any AskUserQuestion or free-text question to you where the answer plausibly lives in: git state, an MCP tool you have connected (decisions / project state / status / signals / roster), your doc-search collections, project + global instruction files, a doctrine / decision register, or a file already in the working tree.

  SKIP: question is purely about your taste / preference / a novel direction with no state precedent; the relevant state has already been read in this turn; you said "stop checking, just do it"; the next tool call will supply the info anyway.
---

# /homework - state pre-flight before asking you

Claude Code reads the relevant state BEFORE asking you a question. Spares you from re-answering things that are already observable; keeps every reply grounded in the current source instead of stale assumption.

## When to fire

**Manual:** you invoke `/homework`, or say "do your homework / check state first / did you check / look before you ask".

**Automatic (CC self-fires):** any moment CC is about to ask you a question that could plausibly be answered from a source listed below. Auto-fire is silent - homework is for CC's own consumption; the visible output to you is a sharper question or no question at all.

## When NOT to fire

- Question is purely about your taste, preference, naming, or a novel direction with no state precedent (this is the legitimate residual use of AskUserQuestion).
- The relevant state has already been read in this turn - do not re-query.
- You have explicitly said "stop checking, just do it" / "ship it".
- Mid-action where the next planned tool call will supply the information anyway - do the call.
- The question is one-screen reversible work and asking will take longer than just doing it.

## Procedure - pick channels by intent class, run in parallel

Cheapest-sufficient state read for the question being asked. Default to 2-3 parallel channel reads; never more than 5.

| Intent in your prompt | Source to read first |
|---|---|
| "what's the status / where are we / give me an update" | `git status -s`, `git log -5 --oneline` |
| "should we ship X / can we land Y" | `git diff --stat`, then any decision-register search for X |
| "what did we decide about X / is there a rule on X" | a decision / doctrine search for X (if you have an MCP register connected), then `Grep` the project + global instruction files for X |
| "what's the vocabulary / canon / brand form for X" | the project instruction file, then your doc-search collections |
| "is X shipped / wired / built / live" | a project-state read (if you have one connected), then `Grep` for the symbol or route |
| "who owns / is on the team for X" | a roster read, if you have one connected |
| "what's pending / escalated / blocked" | any session-start context already injected - re-read it, do not re-query |
| "compliance / legal / standards status of X" | the relevant status read you have available, then a web fetch for any public standards tracker |
| "how does this code work / where is X defined" | `Grep` / `Read` / your code-navigation tool - never ask you to point at a file CC can locate itself |
| "what version / dependency / port for X" | `Read` the relevant config (package.json, pyproject.toml, docker-compose.yml, the project instruction file) |

If a channel above names an MCP tool you do not have connected (decision register, project-state, roster), skip it and fall back to the local equivalent - `git`, `Grep`, `Read`, and your doc search are always available. The point is to read SOMETHING observable before asking, not to require any one integration.

## Output contract

**Auto-fire (CC's own consumption):** no visible report. The output is the sharper next action - a tighter question, a now-answered question that no longer needs asking, or a state-grounded plan instead of an assumption-grounded one.

**Manual invocation:** synopsis + 3-6 short bullets. What state was checked, what each said, what changes about the next move. No prose paragraphs, no H2 headers, no tables.

## Anti-patterns this skill exists to kill

- Asking "which branch are we on / what's the current state" when `git status` is one call away.
- Asking "is feature X built" when a project-state read or a `Grep` is one call away.
- Asking "what did we decide about pricing / vocabulary / scope" when a decision search or a `Grep` of the instruction files is one call away.
- Asking "where is file Y" when Grep / find is one call away.
- Asking "what do the project instructions say about Z" when they are already auto-loaded into the session.

Each of these wastes a turn and proves the state was not consulted.

## Why this matters

Asking you to re-state what's already readable wastes effort - every avoidable question costs a context-laden response that could have been a one-line tool call. `/homework` scopes the state read to the moments where it actually changes the next action (about-to-ask), without burdening every turn with a full state sweep.

## Revision

Amendment-forward only.
