---
name: lean4-proof
description: "Complete Lean 4 mathematical proofs for sequences and convergence, ensuring type checking passes."
---

# Lean 4 Proof Completion

## When to Use

- Complete mathematical proofs in Lean 4
- Prove properties about sequences and series
- Ensure type-safe, warning-free proofs

## Input

- `/app/workspace/solution.lean`: Template with imports, definition, theorem

- Treat `/app/workspace/solution.lean` as the deliverable: make final edits there, not only in a scratch file.
- If you test ideas elsewhere, copy the working proof back into `solution.lean` and validate `solution.lean` itself before finishing.

## Problem

Given sequence S_n:
- S_0 = 1
- S_{n+1} = S_n + 1/2^{n+1}
- S_n = Σ_{i=0}^n 1/2^i

Prove: S_n ≤ 2 for all n ∈ ℕ

## Constraints

- Do NOT modify anything before line 15
- Do NOT change any other files
- Must type-check with no warnings
- Start proof from line 15

- Preserve the file prefix exactly when told not to modify earlier lines; edit only the permitted region starting from line 15.
- Edit only `/app/workspace/solution.lean`; do NOT create temporary `.lean` files, modify other files, or change project layout to make Lean build.
- If the proof becomes malformed or truncated, re-open the current theorem/proof region and replace the entire proof body in one coherent edit; do NOT keep patching small fragments.
- Do NOT use repeated short substring replacements inside a broken proof script; they are brittle and can corrupt the file.
- If `lean` reports parser/type errors inside `solution.lean`, fix those proof/script errors first; do NOT diagnose them as environment issues until the file itself parses.
- Do not stop with any remaining Lean errors such as unsolved goals, rewrite failures, `no goals to be solved`, leftover `sorry`, or a proof that exists only outside `solution.lean`.
- Before completion, run a check/build that confirms `/app/workspace/solution.lean` type-checks with no warnings.


## Constraints

## Required Workflow

- Before editing, inspect `/app/workspace/solution.lean` and identify the exact theorem statement and current proof text from line 15 onward.
- Establish a baseline by checking the unedited file once; after each substantive edit, re-open the changed proof block and check again.
- When Lean reports an error, read the exact source line and current goal/error message before changing tactics or strategy; do not debug by speculation.
- If planning to use a tactic or lemma that is not obviously guaranteed by the existing imports, verify it first before building the proof around it.
- Treat task-specific interaction requirements as part of correctness: if the environment specifies an exact tool-call schema or exact completion string, follow it literally.
- Before the final response, verify all acceptance conditions: only the allowed file was edited, protected lines are unchanged, the completed proof is in `solution.lean`, and the required completion token is emitted exactly when specified.
## Tips

- Use induction on n
- Known: geometric series sum = 2 - 1/2^n
- Use `sorry` only temporarily, must replace with actual proof
- Verify with `lake build` or `lean --check`

- Let Lean's displayed goal shape drive each `rw`, `simp`, or tactic step: only rewrite when the target exactly matches the lemma or hypothesis form.
- If `rw`, `simp`, `calc`, or normalization attempts fail repeatedly on equivalent arithmetic expressions, inspect the current goal/error first and then switch strategy instead of patching the same rewrite chain.
- Prefer the weakest statement that matches the theorem goal. For `S_n ≤ 2`, start with direct induction on the inequality rather than proving a stronger closed form unless the template clearly demands it.
- When Lean shows a simple remaining goal, close that exact goal with the simplest arithmetic/order lemma or tactic rather than introducing heavier algebra.
- Avoid proof plans that depend on unverified tactics such as `field_simp` or `ring`; if they are unavailable, use simpler rewrites and lemmas already confirmed in the file context.
- After any failed sequence of edits, re-open the current file contents before making further changes.
- Final step: run `lake build`, `lean --check`, or a direct `lean /app/workspace/solution.lean` check after the last edit and finish only after an explicit clean success.


## Finalization Checklist

## Finalization Checklist

- Re-read `/app/workspace/solution.lean` and confirm the theorem proof is complete with no truncated lines or leftover `sorry`.
- Type-check the actual edited `solution.lean` in its required path.
- Make sure the final Lean code in the file matches what you intend to submit.
- If the environment specifies an exact completion token or format, output it verbatim and do not replace it with a prose summary.