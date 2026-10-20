---
description: Batch screen problems — binary OPEN or SKIP
allowed-tools: Read, Grep, Glob, Bash, Task, WebFetch, WebSearch
argument-hint: <directory-of-lean-files>
---

Batch screen problems in `$ARGUMENTS`. Binary: OPEN or SKIP.

## Step 1: Scan Directory

List all .lean files with `sorry` in the target directory.

## Step 2: Screen Each

For each file, check: is this an OPEN unsolved conjecture?
- Yes → mark OPEN
- No → mark SKIP

## Step 3: Report

```
BATCH SCREEN: [directory]
Scanned: N files

OPEN (submit bare gap):
  - file1.lean: [theorem name]
  - file2.lean: [theorem name]

SKIP (not open):
  - file3.lean: [reason — solved, in Mathlib, etc.]
```
