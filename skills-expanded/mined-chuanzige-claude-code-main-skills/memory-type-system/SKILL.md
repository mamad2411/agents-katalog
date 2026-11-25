---
name: memory-type-system
description: Use when deciding what information belongs in memory, how to classify it, and what must not be saved because it is derivable from the repo, git history, or current task context
---

# Memory Type System

## Overview

This repository uses a four-type memory taxonomy in `src/memdir/memoryTypes.ts`. The point of the taxonomy is to store durable, non-derivable context, not to duplicate facts that can be recovered from the codebase.

## The Four Types

### user

Save information about the user's role, expertise, preferences, and working style.

Examples:

- senior backend engineer, new to React
- prefers terse answers
- wants explanations framed through observability

### feedback

Save guidance about how work should be done.

Examples:

- do not mock the database in this project
- prefer one bundled PR over many tiny ones
- stop adding summary paragraphs at the end

For feedback memories, include:

- the rule
- why it exists
- how to apply it later

### project

Save ongoing project facts that are not derivable from the current repo state.

Examples:

- merge freeze starts on a specific date
- a rewrite is driven by legal or compliance pressure
- another team is cutting a release branch

Convert relative dates into absolute dates before saving them.

### reference

Save pointers to external systems and where to look next.

Examples:

- bugs are tracked in a specific Linear project
- on-call watches a specific Grafana board
- feedback lives in a particular Slack channel

## What Must Not Be Saved

Do not save:

- code patterns
- architecture already visible in the repo
- file paths that can be rediscovered
- git history or who changed what
- debugging recipes already captured in code or commits
- anything already written in `CLAUDE.md`
- ephemeral task state from the current conversation

If `grep`, `git log`, or reading the repo can answer it, it usually does not belong in memory.

## Selection Heuristic

Save a memory only if it is:

- useful later
- not obvious from the project state
- still meaningful when this conversation is gone

## Structure Heuristic

For `feedback` and `project`, prefer:

1. the rule or fact
2. `Why:`
3. `How to apply:`

That makes the memory durable instead of cryptic.

## Anti-Patterns

- storing codebase summaries as memory
- saving today's activity log
- saving task-local debugging notes
- saving personal preference as team-wide convention

## Done Condition

You have applied this skill correctly when every saved memory fits one of the four types and none of it duplicates information that should instead be recovered from the repo or external source of truth.
