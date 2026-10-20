---
description: Fetch completed Aristotle results, audit, and update DB
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, Task
argument-hint: [slot-number | "all"]
---

Fetch completed Aristotle result(s) for `$ARGUMENTS`.

## Step 0: Reconcile Local Results (NEW — catches missed results)

Before fetching from API, scan for local result files that were never processed into the DB:

```bash
# Find result files not yet reflected in DB
for f in submissions/nu4_final/slot*_result.lean; do
  slot=$(echo "$f" | grep -o 'slot[0-9]*' | head -1)
  db_status=$(sqlite3 submissions/tracking.db "SELECT status FROM submissions WHERE filename LIKE '${slot}%' AND status='submitted'" 2>/dev/null)
  if [ -n "$db_status" ]; then
    sorry=$(grep -cw 'sorry' "$f" 2>/dev/null)
    axiom=$(grep -c '^axiom ' "$f" 2>/dev/null)
    echo "UNPROCESSED: $f (sorry=$sorry, axiom=$axiom, DB still says 'submitted')"
  fi
done
```

If any unprocessed results are found, run `/project:process-result` on each before proceeding.

## Step 1: Run the fetch script

```bash
python3 scripts/aristotle_fetch.py fetch $ARGUMENTS
```

This will:
1. Find UUIDs from `submissions/nu4_final/slot*_ID.txt` files
2. Check status of each via the Aristotle API
3. Download all COMPLETE results to `*_result.lean` files
4. Run basic audit (sorry count, axiom count, negation check)
5. Update `submissions/tracking.db`
6. Print a summary

## Step 2: Deep audit any PROVEN results

For each file marked PROVEN (0 sorry, 0 axiom):
1. Read the full result file
2. Verify no sorry, no axiom, no `admit`, no `Axiom`, no `#check` hacks
3. Confirm the theorem statement matches the intended claim
4. Check that `native_decide` / `decide` were used correctly (not on unsound encodings)

## Step 2b: Extract Knowledge (math-forge)

After auditing each result, extract findings into the knowledge base:

```bash
python3 math-forge/scripts/extract_findings.py submissions/nu4_final/<result_file> --slot <N>
```

This populates knowledge.db with proven theorems, techniques, and failure records for future reference via `mk search` and `mk failed`.

If extraction fails, log a warning but do not block the fetch result.

## Gap Resolution Assessment

After audit, if result is compiled_no_advance (sorry=0, axioms=0, no negation):
- Did this result resolve the OPEN GAP stated in the submission?
- Or did it just compile infrastructure/known math?
- Set target_resolved=1 only if the actual open conjecture was proved.

```bash
sqlite3 submissions/tracking.db "UPDATE submissions SET target_resolved=1 WHERE uuid='<uuid>'"
```

## Step 3: Handle special cases

**NEAR_MISS (1 sorry):**
- Identify which theorem has the sorry
- Assess if the gap is closable locally
- If yes: close it and resubmit as sorry=0

**DISPROVEN (Aristotle negated something):**
- Extract the counterexample
- Record in `false_lemmas` table
- Flag the approach as dead

**FAILED (load errors, many sorry):**
- Check if Aristotle failed to load the file (syntax issue)
- Consider reformulating and resubmitting

## Step 4: Report

Present a clean summary table of all fetched results.
