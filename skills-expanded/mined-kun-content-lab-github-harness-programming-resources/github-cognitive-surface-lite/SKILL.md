---
name: github-cognitive-surface-lite
description: Use when writing readable GitHub Discussions, issues, PR descriptions, review comments, or evidence comments.
---

# GitHub Cognitive Surface Lite

Write GitHub surfaces so a human can review them without reading the whole chat history.

## Core Shape

Use this order:

1. Status.
2. One-sentence result.
3. Context or relationship map.
4. Human-readable content.
5. Evidence.
6. Boundary and risk.
7. Recommended next step.
8. Technical details in a collapsed section if needed.

## Discussion

Must include:

- why this Discussion exists;
- target user or owner;
- in scope;
- out of scope;
- open questions;
- demand confirmation commit when ready.

## Issue

Must include:

- source Discussion or decision;
- goal;
- scope;
- out of scope;
- acceptance criteria;
- evidence requirement;
- close condition.

Layer by size:

- `task` — one executable unit.
- `parent` Epic — control surface; hang sub-issues as native sub-issues; `Refs`, never `Closes`.
- `sub-task` — slice under a parent; `Closes` on completion.
- `truth-source` — frozen standing brief; never claimed, never auto-closed.

## PR

Must include:

- what changed;
- why it changed;
- files or surfaces affected;
- verification;
- review focus;
- linked issue.

## Evidence Comment

Two signals:

- `completion-comment` (`verified`) — task done, ready to close.
- `exploration-comment` (`exploration`) — recording a judgment only, not a completion.

Must include:

- status: ready, partial, or blocked;
- completed items;
- evidence links or file paths;
- not done;
- risks;
- recommendation: close, continue, split, or return to Discussion.

## Writing Rules

- Put the human-readable summary first.
- Put machine details later.
- Do not dump raw logs unless needed.
- Do not write "done" without evidence.
