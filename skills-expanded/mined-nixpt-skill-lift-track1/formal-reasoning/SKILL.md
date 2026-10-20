---
name: formal-reasoning
description: |
  Mathematics and formal reasoning: proofs (e.g. Lean-style), exact
  combinatorial search, planning formalisms (PDDL-like), and deterministic
  algorithmic tasks where partial credit for "almost" is rare. Use for formal
  proof goals, exact optimization/search, and math tasks requiring symbolic
  or verified reasoning — not for soft NLP summarization.
---

# formal-reasoning

Load `safe-agent-scope` before any state-changing action; formal work does not waive sandbox, recipient, or injection rules.

## Why

Formal graders are brittle: a proof that doesn't typecheck is zero; a plan
that misses a predicate is zero. Prefer small verified steps over a large
unchecked leap.

## Procedure

1. **Formalize the goal** — theorem statement, objective, or plan goal atoms.
2. **Inventory axioms/tools** — tactics, solvers, allowed libraries.
3. **Decompose** — lemmas / subgoals / subplans with clear interfaces.
4. **Discharge** — machine-check each piece (compiler, solver, prover).
5. **Assemble** — end-to-end check of the full artifact.
6. **Verify** — run the provided checker/tests; `verify-task-output`.

## Heuristics

- Search problems: encode dominance/pruning; avoid brute force when N explodes
- Proofs: match the style of existing in-repo examples before inventing tactics
- Keep a failing minimal example when stuck — shrink before changing approach

## Anti-patterns

- Handwavy natural-language "proofs" when a machine-checked artifact is required
- Disabling asserts/tests to force success
- Non-deterministic search without a seed when reproducibility matters
