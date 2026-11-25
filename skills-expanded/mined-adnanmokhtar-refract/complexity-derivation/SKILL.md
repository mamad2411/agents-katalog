---
name: complexity-derivation
description: Derive the time and space complexity of code or a design — loops, recurrences, amortized, expected vs worst; cited.
kind: skill
pack: algorithms
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: complexity-derivation

## Premise

Turn a piece of code (or a designed algorithm's structure) into a **cited** time + space complexity — never an intuited one. This is the shared engine the `algorithm-designer` agent, `/design-algorithm`, and `/analyze-complexity` all run on: every `O(...)` it emits names the exact construct it came from (the nested loop at `<path:line>`, the recurrence, the amortized argument), so the bound can be checked rather than trusted.

It does NOT measure runtime — that is the profiler's job (`performance-optimizer`). It reasons about asymptotic growth from structure.

## When to run

- Inside `/analyze-complexity` (derive each hot path's complexity) and `/design-algorithm` (derive the budget + each candidate's class), and in the read steps of `complexity-scan` (the bound a row's `n_max × m_max` arithmetic states) and `/design-algorithm --from-audit` (the class before and after a fix). It derives; it never detects — the detectors are `complexity-scan`, `algorithm-contract-scan` and `numeric-stability-scan`.
- Standalone when a `<path:line>` or a snippet needs a defensible big-O for a review or an ADR.
- NOT for constant-factor questions ("is this 2× faster?") — that needs measurement, not derivation.

## Inputs (precise contract)

| Input | Source | Required |
|---|---|---|
| The code or algorithm structure | `<path:line>` / snippet / pseudocode | YES |
| The growth variable(s) | the caller (`n` = ?, `k` = ?, `V`/`E` for graphs) | YES — an `O(...)` with an undefined variable is meaningless |
| Cost of called operations | the language's container/op guarantees (hash get `O(1)` avg, sort `O(n log n)`, list index-of `O(n)`) | YES — the derivation is only as right as its leaf costs |
| Hotness / scale (optional) | caller / `--scale` | optional — affects whether a bound *matters*, not the bound itself |

## Procedure

1. **Define the variables.** State what `n` (and `k`, `m`, `V`, `E`, ...) are in terms of the input. Refuse to proceed with an undefined variable.
2. **Cost the leaf operations.** Replace every called primitive with its documented cost for the language's standard container: hash map get/put `O(1)` expected, balanced-tree op `O(log n)`, array index `O(1)`, array `indexOf`/`includes`/linear `find` `O(n)`, array `shift`/insert-front `O(n)`, sort `O(n log n)`, heap push/pop `O(log n)`. A wrong leaf cost poisons the whole derivation — this is the #1 error.
3. **Compose sequential + nested.** Sequential statements → the **max** of their costs. A loop → (iterations) × (body cost). **Nested** loops over the same growth → the **product** (two `n` loops → `O(n²)`; an inner loop bounded by the outer index → triangular sum `n(n−1)/2` → still `O(n²)`). A loop whose bound shrinks geometrically (`i *= 2`, halving) → `O(log n)`.
4. **Recurrences for divide-and-conquer / recursion.** Write `T(n) = a·T(n/b) + f(n)` and solve:
   - **Master theorem**: compare `f(n)` to `n^(log_b a)`. (`2T(n/2)+O(n)` → `O(n log n)`; `2T(n/2)+O(1)` → `O(n)`; `T(n/2)+O(1)` → `O(log n)`.)
   - **Recursion tree** when the Master theorem doesn't apply (uneven splits, `T(n)=T(n−1)+O(n)` → `O(n²)`; `T(n)=2T(n−1)+O(1)` → `O(2ⁿ)`).
5. **Amortized when a structure grows or pays-it-forward.** Dynamic-array append, union-find with path compression + union by rank, a monotonic stack/queue where each element is pushed/popped ≤ once. Use the **aggregate** method (total work over `m` ops ÷ `m`) or the **accounting** method (assign credits). Report amortized **and** the worst single op when they differ.
6. **Expected vs worst for randomized + hashed.** Hashing, randomized quickselect/quicksort, skip lists: give the **expected** bound *and* the **worst** (an adversary can force hash collisions to `O(n)` per op on untrusted input — flag it). Don't report only the average for an adversarially-reachable structure.
7. **Space.** Peak **live allocation** + **recursion depth** (stack) + **hidden copies**. A recursive `O(n log n)` sort is `O(log n)` stack; a recursion that copies its **shrinking slice** per level is `O(n)` *peak live* — depth-first, only one root-to-leaf path is live at once, so the copies sum `n + n/2 + n/4 + … = O(n)`; it is `O(n log n)` only when each level copies the **full** size-`n` input regardless of depth (and `O(n log n)` is the *cumulative* allocation either way, not the peak). An immutable update that rebuilds a structure is `O(size)` per update. Count substring/slice copies, closure retention, and accumulator growth.
8. **Simplify + name.** Drop lower-order terms and constants; report the **dominating** term. State worst-case unless asked otherwise and label which case it is. Attach the citation: the `<path:line>` / construct the bound came from.

## Outputs

```
<scope/fn>:
  time:  O(<derived>)  [worst | amortized | expected]   ← from: <loop nesting / recurrence / amortized arg>
  space: O(<derived>)                                    ← from: <peak alloc + recursion depth + copies>
  variables: n = <...>, k = <...>
  notes: <expected-vs-worst gap · adversarial case · assumption (e.g. balanced tree)>
```

A bound with no `← from:` citation is not a valid output of this skill.

## Halt conditions

- **Undefined growth variable** — STOP; an `O(...)` without a defined `n` is meaningless. Ask what scales.
- **Unknown leaf cost** (a called function whose complexity isn't known) — derive it first (recurse into it) or state it as a parameter (`O(C·n)` where `C` = cost of the call); never assume `O(1)`.
- **Input-shape-dependent bound** (BST that may be balanced or skewed, early-exit that may or may not trigger) — report both cases explicitly (`balanced O(log n) / skewed O(n)`), not a single optimistic number.
- **Recurrence the Master theorem doesn't cover** (non-constant `a`/`b`, subtractive splits) — fall back to a recursion tree or substitution; do not force-fit the Master theorem.
- **Asked for runtime, not complexity** — redirect: derivation gives the growth class, not milliseconds; constant factors need `performance-optimizer`'s measurement.

## Related
- agent [`algorithm-designer`](../../agents/algorithm-designer.md) — the consumer; turns derivations into designs + ranked findings.
- commands `/design-algorithm`, `/analyze-complexity` — both run this skill.
- skill `complexity-scan` — cites this skill's derivation for each kept row; its operation-count oracle (V590–V598) is what proves the class.
- rule [`algorithm-principles`](../../rules/algorithm-principles.md) — the budget the derived class is measured against.
