---
description: Screen a problem — binary OPEN or SKIP
allowed-tools: Read, Grep, Glob, Bash, Task, WebFetch, WebSearch
argument-hint: <problem-description, formal-conjectures-file, or url>
---

Screen `$ARGUMENTS` for gap-targeting. Binary decision: OPEN or SKIP.

## Step 1: Load the Problem

Read the problem from `$ARGUMENTS`. Extract the theorem statement.

## Step 2: Is it OPEN?

Check:
1. Is this an unsolved conjecture? (tagged `category research open`, has `answer(sorry)`)
2. Is it NOT in Mathlib? (not already formalized)
3. Is it NOT a known solved result?

## Step 3: Verdict

- **OPEN** → Submit a bare-gap sketch via `/project:sketch`
- **SKIP** → Not an open problem. Move on.

No scoring. No track assignment. No tiers. Just: is the gap open?
