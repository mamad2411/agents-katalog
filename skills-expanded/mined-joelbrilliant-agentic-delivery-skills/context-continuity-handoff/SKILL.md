---
name: context-continuity-handoff
description: Preserves useful state across long agent sessions, context compaction, handoffs, and restarts. Use when compressing context, handing work between agents, resuming after interruption, writing session summaries, or preventing repeated work.
---

# Context Continuity Handoff

## Overview

Use this skill when an agent session may be compressed, reset, handed off, or resumed later.

The goal is not to save everything. The goal is to save the minimum state needed to continue without repeating work or losing decisions.

## When to Use

- Context compaction is near.
- A different agent will continue the work.
- A long-running task pauses overnight.
- A gateway or CLI session must reset.
- The user asks what was decided or what remains.
- Work spans multiple repos, branches, services, or agents.

## Handoff Structure

Use this exact shape:

```text
## Active Task
[Most recent unfulfilled user request]

## Goal
[One paragraph]

## Constraints
[Durable rules and user preferences that matter]

## Completed Actions
[Numbered, evidence-backed actions]

## Active State
[Repo, branch, commit, services, dirty state, running jobs]

## In Progress
[Only current unfinished work]

## Blocked
[Blocker, owner, what would unblock]

## Key Decisions
[Decisions, not every discussion]

## Resolved Questions
[Questions that no longer need asking]

## Pending User Asks
[Direct user asks still unanswered]

## Relevant Files
[Paths and why they matter]

## Remaining Work
[Concrete next steps]

## Critical Context
[Things future agent must not miss]
```

## What to Preserve

Preserve:

- active user request;
- decisions and signoffs;
- constraints and safety rules;
- repo/branch/commit/runtime state;
- exact evidence already gathered;
- blockers and next commands;
- what not to touch.

Do not preserve:

- raw logs unless needed;
- stale todos;
- every tool call;
- secrets;
- temporary speculation;
- solved confusion.

## Quality Bar

A good handoff lets a fresh agent answer:

- What is the task?
- What has already been done?
- What is safe to touch?
- What should not be repeated?
- What is the next tool call?
- What evidence exists?

## Anti-patterns

- Handoff says "continue work" but not what work.
- Long narrative with no active state.
- Losing branch/commit/service details.
- Preserving old instructions that conflict with current user request.
- Recording secrets or credentials.
- Treating completed task history as future instructions.
