---
description: Audit a Lean file from Aristotle for proof validity (sorry, axioms, self-loops, sym2, cover defs)
allowed-tools: Read, Grep, Glob, Bash, Edit, Task
argument-hint: <path-to-lean-file>
---

Audit the Lean file at `$ARGUMENTS` for proof validity. This is a STRICT audit — "proven" is sacred.

## Audit Checklist

Read the file, then check ALL of the following. For each check, output a clear PASS/FAIL with evidence.

### 1. SORRY CHECK
Count all occurrences of `sorry` in the file (exclude comments).
- PASS: 0 sorry
- FAIL: Any sorry found — report count and line numbers

### 2. AXIOM CHECK
Search for `^axiom\s` declarations (line start).
- PASS: No axiom declarations
- FAIL: List each axiom name — these are unproven assumptions, NOT proofs

### 3. SELF-LOOP CHECK (Sym2.mk)
Search for `Sym2.mk` where both arguments are the same variable, e.g., `Sym2.mk (v, v)`, `Sym2.mk (a, a)`.
Also search for shorthand `s(x, x)` patterns in non-comment code lines.
- PASS: No self-loops found
- FAIL: Self-loops are NOT valid SimpleGraph edges — report line numbers

### 4. FINSET.SYM2 CHECK (Context-Aware)
Search for `.sym2` usage in code (not comments). The key distinction: `.sym2` is only UNSAFE when used **constructively in a definition** to create an edge set. It is SAFE in proofs, membership tests, return types, and tactic blocks.

**SAFE patterns (PASS) — ignore these:**
- Inside `by` tactic blocks (indented proof code): `e ∈ t.sym2`, `e ∉ t.sym2` for case analysis
- Lemma/theorem return types: propositions like `∃ e ∈ E, e ∈ t.sym2` or `s(a,b) ∉ X.sym2`
- Universal/existential statements: `∀ e ∈ X.sym2, ...` inside proofs
- Inside `simp [...]`, `decide`, `aesop`, `native_decide` arguments
- `Finset.mem_sym2_iff` — destructures membership
- Filtered: `.sym2.filter (fun e => e ∈ G.edgeFinset)`
- Intersected: `g.sym2 ∩ G.edgeFinset`

**UNSAFE patterns (FAIL) — flag these:**
- `def cover := A.sym2 ∪ B.sym2 ∪ ...` — definition-level union without filter
- `let edges := X.sym2` — binding raw sym2 to a variable used as edge set without filter
- Cover set built from raw `.sym2` without `G.edgeFinset` constraint
- `coverHits` or similar using raw `t.sym2` without edge filtering

### 5. COVER DEFINITION CHECK
If the file defines a triangle cover or edge cover:
- PASS: Cover set `E` has constraint `E ⊆ G.edgeFinset` (or elements proven to be in `G.edgeFinset`)
- FAIL: Cover allows arbitrary `Sym2 V` elements without graph edge constraint
- N/A: File doesn't define a cover

### 6. KNOWN FALSE LEMMA CHECK
Check if the file uses any known-false lemmas by searching for these names:
- `local_cover_le_2` (FALSE — false_lemma #1)
- `external_share_common_vertex` (FALSE — false_lemma #6)
- `link_graph_bipartite` or `konig_theorem` (FALSE — false_lemma #8)
- `not_all_three_edge_types` (NEGATED by Aristotle — K4 counterexample)
- `at_most_two_edge_types` (NEGATED by Aristotle)
- `sym2_cover_cardinality` (FALSE — false_lemma #29)

Also query the database:
```bash
sqlite3 submissions/tracking.db "SELECT lemma_name FROM false_lemmas"
```
- PASS: No known-false lemmas used
- FAIL: Using a disproven lemma — proof is INVALID

### 7. IMPORT/STRUCTURE CHECK
- Does the file import Mathlib properly?
- Does it use `SimpleGraph V` or just set-theoretic `Finset (Fin n)`?
- Note: Phase 1 (concrete Fin n + native_decide) is valid but limited scope

### 8. GAP RESOLUTION ASSESSMENT
Did this result resolve the stated open gap?
- **RESOLVED**: The open conjecture itself is proved (not just sub-lemmas or infrastructure)
- **PARTIAL**: Some progress toward the gap but gap remains open
- **INFRASTRUCTURE**: Known math compiled, gap not advanced
- **N/A**: No gap_statement recorded for this submission

## Output Format

```
╔══════════════════════════════════════════════╗
║  ARISTOTLE OUTPUT AUDIT: <filename>          ║
╠══════════════════════════════════════════════╣
║ 1. Sorry:        PASS (0) / FAIL (N found)  ║
║ 2. Axioms:       PASS / FAIL (list)         ║
║ 3. Self-loops:   PASS / FAIL (lines)        ║
║ 4. Sym2 usage:   PASS / FAIL / WARN         ║
║ 5. Cover defs:   PASS / FAIL / N/A          ║
║ 6. False lemmas: PASS / FAIL (list)         ║
║ 7. Structure:    Phase 1 / Phase 2 / Mixed  ║
║ 8. Gap resolved: RESOLVED / PARTIAL / INFRA  ║
╠══════════════════════════════════════════════╣
║ VERDICT: PROVEN / NEEDS_WORK / INVALID      ║
║ Sorry count: N                              ║
║ Proven theorems: N                           ║
║ Gap status: RESOLVED / PARTIAL / INFRA / N/A║
╚══════════════════════════════════════════════╝
```

## Verdict Rules
- **PROVEN**: All checks PASS, 0 sorry, 0 axiom
- **NEEDS_WORK**: Has sorry but no structural issues (fixable)
- **INVALID**: Has axioms, self-loops, false lemmas, or unsafe sym2 (unfixable without rewrite)

## After Audit

Canonical status enum (2026-05-28):
`submitted | compile_failed | compiled_partial | compiled_no_advance | compiled_advance | disproven`.

If CLEAN COMPILE (0 sorry, 0 axiom), update the database:
```bash
sqlite3 submissions/tracking.db "UPDATE submissions SET status='compiled_no_advance', verified=1, sorry_count=0, proven_count=<N>, notes='...' WHERE filename='<file>'"
```

If NEEDS_WORK (sorry >= 1), update:
```bash
sqlite3 submissions/tracking.db "UPDATE submissions SET status='compiled_partial', verified=NULL, sorry_count=<N>, proven_count=<N>, notes='...' WHERE filename='<file>'"
```

If INVALID (axiom, self-loop, false lemma, unsafe sym2), downgrade:
```bash
sqlite3 submissions/tracking.db "UPDATE submissions SET status='compile_failed', verified=0, sorry_count=<N>, proven_count=<N>, notes='...' WHERE filename='<file>'"
```

Promotion to `compiled_advance` is OPT-IN and requires manual confirmation that the open gap was actually resolved (`target_resolved=1`, `axiomatizes_prior_work=0`, `contribution_statement NOT NULL`).

Report the full audit table and verdict to the user.
