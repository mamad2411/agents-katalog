---
description: Scan for open gaps, state them bare, and submit to Aristotle
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, Task, WebFetch, WebSearch, AskUserQuestion
argument-hint: [--domain nt|algebra|all] [--limit N]
---

Sweep for open gaps and submit bare conjectures. **Gap-targeting only. No proof strategies.**

## Step 1: Parse Arguments

- `--domain`: Filter to `nt`, `algebra`, or `all` (default: `all`, prefer NT/algebra)
- `--limit N`: Max files to scan (default: 20)

## Step 2: Scan for Open Problems

```bash
grep -rl '\bsorry\b' formal-conjectures/FormalConjectures/ --include='*.lean' | head -$LIMIT
```

Or use the screening script:
```bash
python3 scripts/screen_formal_conjectures.py --dir formal-conjectures/ --limit $LIMIT --domain $DOMAIN
```

## Step 3: Filter to OPEN Gaps Only

For each candidate:
1. Is it tagged `category research open`? → CANDIDATE
2. Has `answer(sorry)` (truth unknown)? → CANDIDATE
3. Already in Mathlib or solved? → SKIP
4. Already submitted (check DB)? → SKIP unless prior attempt failed

Only OPEN problems. No known results. No re-proofs.

## Step 4: Check for Dead Ends

```bash
mk failed "<problem keywords>"
sqlite3 submissions/tracking.db "SELECT * FROM false_lemmas WHERE lemma_name LIKE '%<keyword>%'"
```

Skip known dead ends.

## Step 5: Generate Bare-Gap Sketches

For each open gap candidate:
1. Extract the theorem statement
2. Write bare sketch (<=30 lines, no proof strategy)
3. Auto-assign slot number
4. Save to `submissions/sketches/slot<NNN>_<name>.txt`

## Step 6: Submit All

Submit each sketch via `/project:submit`. Fill all available Aristotle slots.

## Step 7: Report

```
SWEEP REPORT
Scanned: N files | Domain: [domain]
Open gaps found: N
Sketches generated: N
Submitted: N (queue: N/5)

| Slot | Problem | Domain | Status |
|------|---------|--------|--------|
| NNN  | ...     | NT     | submitted |
```
