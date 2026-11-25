---
name: beginner-codex-workflow
description: Use when a clinician, researcher, or beginner asks Codex to inspect, modify, explain, or verify code.
---

# Beginner Codex Workflow

## Goal

Make coding-agent work understandable to clinicians and beginners without sacrificing engineering discipline.

## Required Behavior

1. Explain what you are about to inspect.
2. Read the relevant files before proposing changes.
3. Use simple words for technical concepts.
4. Make the smallest useful change.
5. Verify with a command, screenshot, or explicit manual check.

## Output Pattern

```md
## What I checked

## What I changed

## How I verified it

## What you can do next
```

## Do Not

- Rewrite large parts of a project without need.
- Hide errors behind vague language.
- Assume the user knows programming jargon.
- Commit, push, publish, or delete without explicit confirmation.

