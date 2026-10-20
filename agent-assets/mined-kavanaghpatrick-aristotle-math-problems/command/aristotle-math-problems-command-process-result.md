---
description: Process an Aristotle result file — extract output, audit, and update DB in one step
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, Task
argument-hint: <path-to-aristotle-output-or-uuid>
---

Process the Aristotle result at `$ARGUMENTS`. This combines extraction + full audit + DB update.

## Step 1: Locate and Read the File

If `$ARGUMENTS` is a UUID, find the file:
```bash
find submissions/ -name "*$ARGUMENTS*" -type f 2>/dev/null
```

If it's a file path, read it directly. The file should be a `.lean` file (Aristotle output).

## Step 2: Extract Key Metrics

Count from the actual file content (NEVER trust DB values):
- **sorry count**: `grep -c '\bsorry\b'` (exclude comments)
- **proven count**: Count theorem/lemma blocks that don't contain sorry
- **axiom count**: `grep -c '^axiom '`
- **total declarations**: Count all theorem/lemma/def declarations
- **lines of code**: `wc -l`

## Step 3: Run Full Audit

Run the complete audit checklist (same as `/project:audit`):

1. **Sorry** — count and locate
2. **Axioms** — any `axiom` declarations
3. **Self-loops** — `Sym2.mk(v,v)` or `s(v,v)` in code
4. **Finset.sym2** — context-aware classification:
   - SAFE: inside `by` tactic blocks, lemma return types (`∈`/`∉`/`∃`), `simp`/`decide` args, filtered (`.filter`/`∩ G.edgeFinset`), `mem_sym2_iff`
   - UNSAFE: **only** in constructive definitions (`def cover := A.sym2 ∪ B.sym2` without filter, `let edges := X.sym2` without filter)
   - Rule: `.sym2` in proofs/tactics/propositions = SAFE. Only UNSAFE when creating edge sets in definitions.
5. **Cover definitions** — must have `E ⊆ G.edgeFinset`
6. **Known false lemmas** — check against `false_lemmas` table
7. **Structure** — Phase 1 (Fin n) vs Phase 2 (SimpleGraph V)

## Step 4: Determine Verdict

Canonical status enum (2026-05-28):
`submitted | compile_failed | compiled_partial | compiled_no_advance | compiled_advance | disproven`.
Note: `compiled_advance` is OPT-IN — only set when target_resolved=1, axiomatizes_prior_work=0,
and contribution_statement is filled. `/process-result` defaults to `compiled_no_advance`.

| Condition | Verdict | DB Status |
|-----------|---------|-----------|
| 0 sorry, 0 axiom, all checks pass | **CLEAN COMPILE** | `compiled_no_advance`, `verified=1` |
| Aristotle negated the conjecture | **DISPROVEN** | `disproven`, `verified=NULL` |
| sorry >= 1, no structural issues | **PARTIAL** | `compiled_partial`, `verified=NULL` |
| Has axiom, self-loops, false lemmas, or unsafe sym2 | **INVALID** | `compile_failed`, `verified=0` |
| Gap was actually resolved (manual confirm) | **ADVANCE** | `compiled_advance`, `verified=1`, `target_resolved=1` |

## Step 5: Update Database

Determine the slot number from the filename and update/insert:

```bash
sqlite3 submissions/tracking.db "
UPDATE submissions SET
  status='<verdict_status>',
  sorry_count=<actual_sorry>,
  proven_count=<actual_proven>,
  verified=<0_or_1_or_NULL>,
  notes='<audit_summary>'
WHERE filename='<filename>';
"
```

If no existing entry, insert:
```bash
sqlite3 submissions/tracking.db "
INSERT INTO submissions (filename, status, sorry_count, proven_count, verified, frontier_id, notes)
VALUES ('<filename>', '<status>', <sorry>, <proven>, <verified>, 'nu_4', '<notes>');
"
```

## Step 6: Report

Output the full audit table:

```
╔══════════════════════════════════════════════╗
║  RESULT: <filename>                          ║
╠══════════════════════════════════════════════╣
║ Sorry:    N  │  Proven: N  │  Axioms: N     ║
║ Lines:    N  │  Declarations: N              ║
╠══════════════════════════════════════════════╣
║ 1. Sorry:        PASS/FAIL                  ║
║ 2. Axioms:       PASS/FAIL                  ║
║ 3. Self-loops:   PASS/FAIL                  ║
║ 4. Sym2 usage:   PASS/FAIL/WARN             ║
║ 5. Cover defs:   PASS/FAIL/N/A              ║
║ 6. False lemmas: PASS/FAIL                  ║
║ 7. Structure:    Phase 1/2                  ║
╠══════════════════════════════════════════════╣
║ VERDICT: PROVEN / NEAR_MISS / NEEDS_WORK / INVALID ║
║ DB Updated: YES                              ║
╚══════════════════════════════════════════════╝
```

If NEAR_MISS (1 sorry), also identify:
- Which theorem/lemma has the sorry
- What the sorry is trying to prove
- Suggest: try `exact?`, `simp?`, `omega`, `native_decide` (Fin n) to close it locally, then resubmit with sorry=0

## Gap Resolution Assessment

Assess: did this result resolve the stated open gap?
- Check the gap_statement in tracking.db
- Compare the proven theorems in the result against the open conjecture
- target_resolved=1 ONLY if the open problem itself was resolved (not sub-lemmas)

## Step 7: Extract Knowledge (math-forge)

After audit and DB update, extract findings into the math-forge knowledge base:

```bash
python3 math-forge/scripts/extract_findings.py <result_file> --slot <N>
```

This indexes proven theorems, proof techniques, and failure records so future sketches can query prior knowledge via `mk search` and `mk failed`.

If extraction fails, log a warning but do not block the process-result workflow.
