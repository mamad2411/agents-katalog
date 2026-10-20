---
description: Write a bare-gap sketch for INFORMAL submission — state the open gap, nothing else
allowed-tools: Read, Grep, Glob, Bash, Task, WebFetch, WebSearch, Write, AskUserQuestion
argument-hint: <problem-description, formal-conjectures-file, or url>
---

Write a bare-gap sketch for `$ARGUMENTS`. State the open gap. Nothing else. Let Aristotle find the path.

## Step 1: Identify the Gap

Load the problem from `$ARGUMENTS`:
- **File path**: Read it, extract the theorem statement
- **URL**: Fetch and extract the conjecture
- **Description**: Parse the mathematical claim

Confirm it's OPEN (not in Mathlib, not solved). If it's a known result, STOP — we don't sketch known results.

## Step 2: Check for Dead Ends

```bash
mk failed "<problem keywords>"
mk find "<problem_id>"
sqlite3 submissions/tracking.db "SELECT * FROM false_lemmas WHERE lemma_name LIKE '%<keyword>%'"
```

If the problem is a known dead end, STOP and report.

## Step 3: Write the Bare-Gap Sketch

Write a .txt file. **<=30 lines. No proof strategy. No key lemmas. No approaches.**

```
OPEN GAP: [Problem Name]
Source: [formal-conjectures path or Erdos number]
Domain: [nt / algebra / combinatorics / analysis]

[1-3 sentence English statement of the unsolved conjecture]

theorem problem_name (vars : Types) : conclusion := by sorry

Status: OPEN. [One sentence on what's known — "verified to N=10^6", "open since 1971"]
```

That's the entire sketch. Nothing else.

## Step 4: Assign Slot and Save

```bash
sqlite3 submissions/tracking.db "SELECT COALESCE(MAX(CAST(SUBSTR(filename, 5, INSTR(SUBSTR(filename,5),'_')-1) AS INTEGER)), 577) + 1 FROM submissions WHERE filename LIKE 'slot%'"
```

Save to `submissions/sketches/slot<NNN>_<name>.txt`

## Step 5: Report

```
SKETCH: <problem name>
File: submissions/sketches/slot<NNN>_<name>.txt
Lines: NN (<=30)
Domain: NT / Algebra / etc
Next: /project:submit <file>
```
