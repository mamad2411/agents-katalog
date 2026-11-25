---
name: pack-skill
description: Solve any problem in the philosophical family of the knapsack problem (背包问题) using the unified state-design framework from 崔添翼《背包问题九讲》. Use whenever a problem reduces to "choose a subset/multiset of items under a capacity-like cost to optimize a value-like objective" — including 0/1 pack, unbounded/complete pack, bounded/multiple pack, mixed pack, 2-D cost pack, grouped pack, dependency pack (主件/附件, tree-shaped), generalized items (泛化物品), subset-sum / can-it-fill-exactly, counting feasible or optimal schemes, recovering the chosen subset, lexicographically smallest plan, and Kth-best value. Trigger words — 背包/knapsack, subset sum, "choose items with weight/cost ≤ W to maximize value", "ways to make change", "partition into K groups", "limited copies", "items depend on each other", "fill exactly", coin change counting, NOIP-style 金明的预算方案 / 采药 / 装箱问题.
---

# pack-skill — 背包问题九讲 in skill form

## What "philosophically a knapsack problem" means

A problem belongs to this family iff it can be cast as:

> Given a finite collection of **items**, each consuming some **cost(s)** when taken and yielding some **value**, choose a feasible selection under a **capacity** to optimize an aggregate of values.

Under that frame, every variant reduces to one master DP: `F[i, v] = combine over item-i policies of F[i−1, v − cost(policy)] ⊕ value(policy)`. The job of this skill is to (a) recognize the variant, (b) write the right state + transition + iteration order, (c) handle the question-form (max value / count / output plan / Kth-best).

## Workflow — apply in order

1. **Recognize the variant.** Read `references/01-recognize.md` and run the decision tree there. Identify: how many copies per item, single/multi cost, item interactions (exclusive groups, dependencies), and what the question asks.
2. **Design the state.** Read `references/02-state-design.md`. Decide: dimensions of `F`, init values (max-value vs exact-fill), and 1-D space compression direction.
3. **Pick the canonical procedure** for each item type and call it in the right loop order. The procedures are reusable Python functions in `scripts/pack_primitives.py`:
   - `zero_one_pack(F, C, W)` — item taken 0 or 1 time
   - `complete_pack(F, C, W)` — item taken unlimited times
   - `multiple_pack(F, C, W, M)` — item taken 0..M times (binary-splitting)
4. **Handle the question form.** Output plan, count schemes, count optimal schemes, Kth-best — see `references/11-variations.md` and the corresponding scripts.
5. **Verify correctness on the simple cases first** — for any non-trivial setup, brute-force enumerate up to N≤20 and diff against the DP. `scripts/pack_primitives.py` includes a `brute_max` helper for this.

## Reference map

Read the file matching the variant you identified in step 1. Each is self-contained.

| Variant | Reference file | Script |
|---|---|---|
| Recognize / decision tree | `references/01-recognize.md` | — |
| State design, init, space opt | `references/02-state-design.md` | — |
| 01 pack (0/1) | `references/03-zero-one.md` | `scripts/solve_01.py` |
| Complete pack (unbounded) | `references/04-complete.md` | `scripts/solve_complete.py` |
| Multiple pack (bounded M_i) | `references/05-multiple.md` | `scripts/solve_multiple.py` |
| Mixed (01 + complete + bounded) | `references/06-mixed.md` | `scripts/solve_mixed.py` |
| 2-D cost (two capacities) | `references/07-2d-cost.md` | `scripts/solve_2d.py` |
| Grouped (mutually exclusive groups) | `references/08-grouped.md` | `scripts/solve_grouped.py` |
| Dependency (main / accessory, tree) | `references/09-dependency.md` | `scripts/solve_dependency.py` |
| Generalized items (泛化物品 abstraction) | `references/10-generalized.md` | — |
| Question variations | `references/11-variations.md` | `scripts/count_schemes.py`, `scripts/count_optimal.py`, `scripts/output_solution.py`, `scripts/kth_optimal.py` |

## The five invariants (read once, never forget)

These come straight from chapters 1–9. They are the rules every variant obeys.

1. **Master transition.** `F[i,v] = max{ F[i-1, v - k·Cᵢ] + k·Wᵢ }` over the legal copy-counts `k` for item `i`. Every variant differs only by which `k` are legal.
2. **1-D direction encodes copies.**
   - 0/1 item → iterate `v` **descending** from `V` to `Cᵢ` (so each Wᵢ is added at most once).
   - Unbounded item → iterate `v` **ascending** from `Cᵢ` to `V` (so Wᵢ may cascade).
   - Bounded → binary-split into `O(log Mᵢ)` 0/1 items.
3. **Init encodes "exact fill" vs "≤ capacity".**
   - Must fill exactly: `F[0]=0, F[1..V] = -∞`.
   - Just ≤ V: `F[0..V] = 0`.
4. **Grouped/dependency = mutually exclusive policies per unit.** Loop order is `for group → for v descending → for item-in-group`, never permute these three.
5. **泛化物品 (generalized item) is the universal abstraction.** Any item / group / subtree corresponds to a function `h: [0..V] → value`. "Sum" of two generalized items is `f(v) = max_{0≤k≤v} h(k)+l(v-k)`, `O(V²)`. Most "hard-looking" knapsacks are just a sum of generalized items.

## Common pitfalls

- **Wrong iteration direction** → silently overcounts (treats 0/1 as unbounded) or undercounts.
- **Forgetting the exact-fill init** → answers max-value when the problem says "fill exactly".
- **Grouped pack with v-loop inside item-loop** → lets multiple items of the same group be taken.
- **Multiple pack with M·C ≥ V** → just call `complete_pack`; don't binary-split.
- **Dependency pack as plain group** → wrong; you must first 0/1-DP the accessory set into a generalized item of length `V − C_main + 1` (see chapter 7).
- **Counting schemes** → replace `max` with `sum`, and init `F[0,0]=1` (or `F[0]=1` in 1-D).
- **Lex-smallest plan** → renumber items as `x ← N+1−x` first, then run the standard recovery (chapter 9.2).

## Quick start — solving a fresh problem

```text
Q: N items, each with weight wᵢ and value vᵢ, knapsack capacity W, each item used at most once.
   Maximize total value.
```

This is plain 0/1 pack. Run:

```bash
python3 scripts/solve_01.py --capacity W --items "w1,v1; w2,v2; ..."
```

Or import the primitive:

```python
from pack_primitives import zero_one_pack
F = [0] * (W + 1)
for c, w in items:
    zero_one_pack(F, c, w)
print(F[W])             # max value with capacity ≤ W
```

For "fill exactly W": initialize `F = [0] + [float('-inf')] * W` instead.

## When the problem doesn't look like a knapsack but is one

Recognize these disguises (each is treated in `references/01-recognize.md`):

- **Coin change — number of ways**: complete pack + `sum` instead of `max`, `F[0]=1`.
- **Subset sum / partition equal subset**: 0/1 pack with W=value, ask "is `F[target]` reachable".
- **Cutting rod**: complete pack with `C = length, W = price`.
- **Target sum / +/- signs**: shift to subset-sum form `target = (S + target_diff)/2`.
- **NOIP 金明的预算方案**: dependency pack (main + ≤2 accessories) — see chapter 7.
- **NOIP 采药 / 装箱问题**: textbook 0/1 pack.
- **Multi-dimensional resource scheduling** (cost in cash AND time, etc.): 2-D cost pack.

## Verification

Whenever you write a new knapsack DP, brute-force check it on small inputs:

```python
from pack_primitives import brute_max_01
assert dp_answer == brute_max_01(items, W)
```

`scripts/pack_primitives.py` ships `brute_max_01`, `brute_max_complete`, `brute_max_multiple` for this.
