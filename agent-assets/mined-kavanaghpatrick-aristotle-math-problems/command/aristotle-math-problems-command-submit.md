---
description: Submit a bare-gap sketch to Aristotle — gap-targeting gate -> auto-context -> submit INFORMAL
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, Task, AskUserQuestion
argument-hint: <path-to-sketch.txt> [slot_number] [--context context_slot]
---

Submit `$ARGUMENTS` to Aristotle. **Gap-targeting ONLY. INFORMAL .txt only.**

## Step 1: Parse Arguments

Extract file path and optional slot number from `$ARGUMENTS`.
If no slot number given, extract from filename (e.g., `slot674_name.txt` -> 674).
Extract optional `--context <slot>` for explicit context file.

If `$ARGUMENTS` is empty, ask:
- **Question**: "What sketch should we submit?"
- **Header**: "File"
- **Options**:
  - "Browse sketches" — "Look for .txt files in submissions/sketches/"
  - "I'll provide a path" — "Enter a specific file path"

Validate the file exists.

## Step 2: Gap-Targeting Gate (HARD BLOCK)

The sketch MUST pass `check_gap_targeting()`:
- .lean files → REJECTED (gap-targeting = INFORMAL .txt only)
- >30 non-blank lines → REJECTED (strip proof strategy, state only the gap)
- Strategy keywords (Proof Strategy, Key Lemma, APPROACH, etc.) → REJECTED
- Empty file → REJECTED

**No override. No --force flag. Rejection is final.**

If the sketch is a falsification (contains "disprove", "counterexample", etc.), it passes as `submission_type=falsification`.

## Step 3: Auto-Context

Gather prior Aristotle results for this problem:
```bash
mk context <problem_id>
```

Or query directly (use artifact presence, NOT status — the status enum changes, output_file does not):
```bash
sqlite3 submissions/tracking.db "SELECT output_file FROM submissions WHERE problem_id LIKE '%<id>%' AND output_file IS NOT NULL AND output_file != '' AND status != 'compile_failed' AND (verified IS NULL OR verified != 0) ORDER BY completed_at DESC"
```

Merge auto-detected context with any explicit `--context` files. All context passed via `context_file_paths`.

## Step 4: Pre-Flight Checks

- **False lemmas**: `sqlite3 submissions/tracking.db "SELECT lemma_name FROM false_lemmas"`
- **Prior attempts**: How many times submitted before?

## Step 5: Submit INFORMAL

Delegate to `safe_aristotle_submit.py` which handles gap-targeting gate, queue checks, retry logic, lockfile, dedup, and transaction logging:

```bash
python3 scripts/safe_aristotle_submit.py <file> <slot> --informal --context <context_file_1> --context <context_file_2>
```

Use context files gathered in Step 3. If no context files, omit `--context` flags.

## Step 6: Track

```bash
python3 scripts/aristotle_fetch.py track <slot> <uuid> "<description>"
```

```bash
sqlite3 submissions/tracking.db "
UPDATE submissions SET gap_statement='<gap>', submission_type='<type>'
WHERE uuid='<uuid>';
"
```

## Step 7: Confirm

```
SUBMITTED: <filename>
Mode: INFORMAL (gap-targeting)
Project ID: <uuid>
Context: N prior result files attached
Queue: N/5 | Monitor: /project:status
```
