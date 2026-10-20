---
name: minizinc
description: >-
  Expert MiniZinc modeling for constraint satisfaction and combinatorial
  problems.
  You MUST load this skill when addressing constraint satisfaction or combinatorial problems using MiniZinc.
license: MIT
---
<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

# MiniZinc Modeling

## WHEN TO USE

- Addressing constraint satisfaction, scheduling, assignment, or combinatorial problems.
- Need to apply expert advanced modeling techniques in MiniZinc (tight domains, globals, symmetry breaking, search annotations, channeling, etc.).
- User requests creation, refinement, debugging, or optimization of MiniZinc models.
- When manual resolution of a combinatorial challenge is required: use the MiniZinc model as a logical framework to derive and verify the solution step-by-step without premature termination.
- When preparing to solve a complex logical or combinatorial problem: dry-write a MiniZinc model first to explicitly map and visualize the constraints before proceeding with the actual resolution.

## WHEN NOT TO USE

- For solving continuous, non-linear optimization problems where specialized solvers (like IPOPT or interior point methods) are strictly required.
- When you just need to run an existing model without modifying or analyzing its structure.
- For simple procedural logic tasks that do not involve constraint solving or combinatorial search.

## Common Pitfalls

- **Loose Domains**: Failing to specify tight bounds (e.g., using `var int` instead of `var 1..n`), which exponentially increases the search space.
- **Ignoring Symmetry**: Not applying `lex_lesseq` or `symmetry_breaking_constraint`s on identical entities, leading to the solver wasting time exploring identical branches.
- **Hardcoding Data**: Embedding specific instance values directly in the `.mzn` file instead of separating them into a `.dzn` parameters file.

## Core Process (execute autonomously, no user prompts)

1. **Model Skeleton** – Start every file with:

   ```minizinc
   include "globals.mzn";
   % parameters + tight instance data (prefer .dzn)
   % decision variables with tightest feasible domains
   % constraints (globals first, then custom predicates)
   solve satisfy;
   % solve :: int_search(vars, first_fail, indomain_min) satisfy;
   % solve minimize objective;
   output [ ... ];
   ```

2. **Tight Domains + Propagation** – Declare every `var` with explicit
   bounds or enum index sets immediately (`var 1..n`, `var set of 1..k`,
   `opt int`). Use `lb`, `ub`, `dom` reflection to derive tighter bounds dynamically.

3. **Global Constraints First** – Prefer `all_different`, `global_cardinality`,
   `cumulative`, `disjunctive`, `circuit`, `regular`, `table`, `lex_lesseq`
   over raw loops. For grids/matrices, use `all_different` on row/column slices:
   `forall(i in 1..n)(all_different(row(grid, i)))`.
   Add redundant constraints annotated with `:: redundant_constraint` and
   symmetry-breaking constraints annotated with
   `:: symmetry_breaking_constraint` liberally for free propagation.

4. **Symmetry Breaking** – Always apply lexicographic ordering on identical
   objects (`lex_lesseq` or `lex_less` on arrays of symmetric vars).

5. **Search Annotations** – Default: `solve :: int_search([vars], first_fail, indomain_min) satisfy;`.
   Tune only after profiling: `dom_w_deg` + `indomain_median` for hard instances.

6. **Reusable Primitives** – Extract repeated sub-structures into
   `predicate` / `function` (e.g., `no_overlap`, `channeling`, custom table
   constraints). Keep bodies <30 LOC.

7. **Advanced Techniques (use in order of impact)**
   - **Grid Patterns**: Model 2D structures using `array[1..N, 1..N]` and
     comprehensions like `[grid[r, c] | r in i*S+1..i*S+S, c in j*S+1..j*S+S]`
     for sub-blocks. Use `row(grid, i)` and `col(grid, j)` for matrix slice
     iteration in globals. Use `show2d(grid)` or `format` for readable
     matrices.
   - **Channeling**: Model same problem in two views + link with `inverse`, `element`, or `lex` constraints.
   - **Let + Local Constraints**: Hide auxiliary vars inside large expressions.
   - **Optionals & Absents**: Use `opt int` + `occurs` / `absent` for optional assignments.
   - **Table + Regular**: Encode complex feasibility with `table` or `regular` automata.
   - **Data Separation**: Keep instance data in `.dzn` or `-D` flags; never hard-code.

## Autonomous Verification Loop

- Solve tiny instance first (tracer bullet).
- If UNSAT: add `trace` debug statements, relax one constraint at a time, re-solve.
- If SAT but unexpected: assert post-solution invariants via `constraint` or `trace` in output.
- Run with Gecode → Chuffed → HiGHS; compare solutions.
- If performance <1s on medium instance: tighten domains or add redundant globals.
- Final output must include human-readable `show` for all decision vars.

## Diagnostics & Patterns

- **Common Smells** → fix immediately: loose domains, raw `forall` loops
  replaceable by globals, missing symmetry, no search annotation.
- **Output Template**: `output ["solution = \(x)", ...];`
  (never print raw decision vars).
- **Comprehensions**: `forall(i,j in 1..n where i<j)(x[i] != x[j]);`
  – most restrictive generator first.

## What to Avoid

- Never use wide domains or `var int` without bounds.
- Never hard-code instance values in model (use parameters).
- Never omit `globals.mzn`.
- Never rely on default search for non-trivial models.
- Never leave symmetry unaddressed in symmetric problems.

## Limitations & Safety

- MiniZinc is declarative: never embed imperative loops or side-effects.
- For very large instances, split into staged models or use external data generators.
- Safety-critical scheduling: always add explicit resource bounds and
  post-solution validation predicates.
