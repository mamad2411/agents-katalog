---
name: estimate-project
description: Run a structured estimation session that produces a valid estimate.v1 artifact — decompose the work, collect three-point ranges, compute PERT expected value and p50/p80/p95, sanity-check against the project's own delivery history, and declare a confidence class. Use when asked how much something will cost or how long it will take, when a plan needs numbers before commitment, or when an existing estimate must be re-baselined.
user-invocable: true
argument-hint: "[scope or path to plan.v1] [--class order-of-magnitude|budgetary|definitive]"
agent: foundry-economics:cost-engineer
model: opus
effort: high
metadata:
  foundry.vertical: economics
  foundry.io: "plan.v1 -> estimate.v1"
license: Apache-2.0
---

# Estimate a project

Produces a **range with named assumptions**, not a number. The output is an `estimate.v1`
artifact that a sceptical reader can reconstruct from the worksheet by hand.

**Not financial advice.** Analytical decision support. Contractual commitments need
professional review.

## The rule that makes this skill worth using

Every figure carries its provenance marker, always:

- `[measured: <path or command>]` — read from project data
- `[given: <who/when>]` — supplied by a human in this session
- `[ASSUMPTION — confirm]` — an assumption someone must confirm

Anything unsourced is written as a visible placeholder — `<<TBC: blended day rate, EUR/day>>` —
never as a plausible number. If you catch yourself about to write "roughly 5 days" for
something nobody said, stop and write `<<TBC: effort for X>>` instead.

## Step 0 — Decide whether to estimate at all

Skip this skill and say so when:

- The scope is one sentence and nobody will decompose it. Estimating undefined scope produces
  a number that will be quoted forever and was never true. Decompose first, or refuse.
- The decision does not depend on the number. If the work is happening regardless, the estimate
  is theatre.
- Someone wants a single number for a contract. Then this skill is the input to a commercial
  decision, not the decision — say which percentile is being committed to and who carries the gap.

## Step 1 — Establish the basis of estimate

Write these down before any number is produced. They go into `assumptions[]`.

| Item | Why it matters |
|---|---|
| Scope statement, one paragraph | The estimate is only valid for this scope |
| What is **excluded** | Goes to `excluded[]`; the most-read part of any estimate |
| Unit: hours, days or EUR | `estimate.v1` allows only these three; mixed units need separate items |
| Rate basis per role | A single blended rate hides mix risk — state the roles |
| Currency | `estimate.v1.currency`, default EUR |
| Calendar assumptions | Working days per month, holidays, availability as a fraction of FTE |
| Confidence class target | Order-of-magnitude / budgetary / definitive — see step 6 |

Retrieve prior context cheaply with the `foundry` MCP server rather than reading files:
`memory_search` for facts of type `metric` or `decision` about rates and past velocity, and
`blackboard_read` for any existing `plan.v1`.

## Step 2 — Decompose

Split until each leaf is work one role could finish inside a normal sprint and a person can
picture doing. Target **8–60 leaves**. Fewer means the ranges are meaningless; more means the
decomposition costs more than the estimate is worth.

Load `references/wbs-checklist.md` and walk it. It exists because the overrun is almost never
in the feature — it is in the environment setup, the second data migration, the rework loop,
the compliance evidence, the runbook, the rollback rehearsal and the stabilisation window.

Each leaf gets: `label`, `role`, `unit`. Write them straight into
`.foundry/economics/estimate-worksheet.csv` using `references/templates/estimate-worksheet.csv`.

## Step 3 — Collect three points per leaf

Ask in this order, always: **pessimistic first, then optimistic, then likely.** Asking for the
likely value first anchors the other two and collapses the range — this ordering is the whole
technique.

Frame them concretely, not statistically:

- Pessimistic — "everything that realistically could go wrong does: the API is undocumented,
  the data is dirtier than expected, the reviewer is on leave. Not an asteroid."
- Optimistic — "everything goes right, no interruptions, no surprises."
- Likely — "the single most probable outcome."

Two gates on every leaf:

- `p / o < 1.5` → false precision. Nobody knows software effort that well. Push back.
- `p / o > 10` → this is not one piece of work. Split it.

## Step 4 — Compute

```
Eᵢ   = (oᵢ + 4·mᵢ + pᵢ) / 6
σᵢ   = (pᵢ − oᵢ) / 6
E_total   = Σ Eᵢ
Var_indep = Σ σᵢ²
σ_total   ≈ σ_indep · √(1 + ρ·(n − 1))      uniform pairwise correlation ρ

p50 ≈ E_total
p80 ≈ E_total + 0.84 · σ_total
p95 ≈ E_total + 1.64 · σ_total
```

**Choose ρ deliberately and state it.** `ρ = 0` claims a bad week hits exactly one task.
Shared causes — one team, one architecture, one unproven platform, one absent stakeholder —
make that false. The full derivation, the normal-approximation caveat and worked examples are
in `references/pert-math.md`; read it before defending a number.

Convert to money only at the end, per role:
`cost = Σ (effortᵢ × rate(roleᵢ))`, each rate `[given]` or a placeholder.

## Step 5 — Reference-class sanity check

Your decomposition can only contain work you thought of, so it is structurally optimistic.
Correct it with **this project's own record** — never an invented industry multiplier.

```
upliftᵢ    = actualᵢ / estimatedᵢ
uplift_p80 = 80th percentile of {upliftᵢ}
E_adjusted = E_total × uplift_p80
```

Sources, in order of preference, all of which you actually have:

1. `.foundry/blackboard/*/cost-engineer.json` — past estimates
2. `memory_search` for facts of type `metric`
3. `git log --format='%ad %s' --date=short`, tag-to-tag intervals
4. `gh issue list --state closed --json number,createdAt,closedAt` when `gh` is installed

Reconcile out loud: if `E_adjusted > p80`, your bottom-up range is too narrow — widen it and
name the omission the history implies. With **fewer than five** comparable past items, declare
the reference class too thin and use it as a directional challenge only.

No history at all → say "no reference class available in this project" and cap the confidence
class at order-of-magnitude. Method detail in `references/reference-class.md`.

## Step 6 — Declare the confidence class

Per AACE International Recommended Practice 18R-97, estimate accuracy tracks **scope maturity**,
not effort spent estimating:

| Label | AACE class | Scope maturity | Fit for |
|---|---|---|---|
| Order-of-magnitude | Class 5–4 | concept, ≤ ~10% defined | screening, direction |
| Budgetary | Class 3 | design in progress, ~10–40% defined | budget lines, funding requests |
| Definitive | Class 2–1 | design largely complete, ≥ ~65% defined | contractual commitment |

Cite the class and **your own computed interval**. Do not quote an accuracy band you did not
derive from your own σ. State the maturity evidence: which requirements are signed off, which
interfaces are specified, which unknowns remain open.

`estimate.v1` sets `additionalProperties: false` and has no field for this, so it goes in as
the **first** element of `assumptions[]`, verbatim:

```
"Confidence class: budgetary (AACE 18R-97 Class 3). Scope ~30% defined: 12 of 18 requirements signed off, external payment API contract still unspecified."
```

## Step 7 — Contingency from risks, not from a round percentage

For each genuinely uncertain driver, emit a `risk.v1`:
`exposureEur = probability × impactEur`, with `mitigation` and an accountable `owner`.

```
contingency = Σ exposureEur of the risks you chose to carry
```

That is defensible at a budget review. "Plus 20%" is not — it either has no basis or hides a
risk somebody should be managing.

## Step 8 — Write and validate

Emit via the `blackboard_write` MCP tool, which validates before writing:

```
wave:   estimation
agent:  cost-engineer
schema: estimate.v1
```

Schema constraints that actually bite:

- `items[].unit` ∈ {`hours`, `days`, `eur`} only
- `assumptions` needs `minItems: 1`; `assumptions[0]` is the confidence class
- `excluded[]` is optional in the schema and **required by this skill**
- `confidenceInterval` holds only `p50`, `p80`, `p95`

Companion workings — the full table, formulas and the reference-class reconciliation — go to
`.foundry/blackboard/estimation/cost-engineer.md`, rendered from
`references/templates/estimate-rollup.md`. Return to the caller only the two paths plus a
summary of ≤ 300 tokens (AUTHORING §2).

## Exit criteria

- [ ] 8–60 leaves, each with `o`, `m`, `p`, `role`, `unit`
- [ ] No leaf with `p/o < 1.5` or `p/o > 10`
- [ ] `E_total`, `σ_total`, `p50`, `p80`, `p95` computed, workings shown
- [ ] ρ stated with a reason
- [ ] Reference-class check performed, or its absence explicitly declared
- [ ] `assumptions[0]` is the confidence class with scope-maturity evidence
- [ ] `excluded[]` non-empty
- [ ] Contingency derived from `risk.v1` exposures, not a flat percentage
- [ ] Zero unlabelled numbers
- [ ] `blackboard_write` returned VALID
- [ ] The single assumption that would most change the total is named in the summary
- [ ] The commitment percentile is stated, with who carries the gap between p50 and it

## What this skill deliberately does not cover

- **Scheduling.** No critical path, no resource levelling, no Monte Carlo over a precedence
  network. This aggregates cost, it is not a scheduling engine.
- **Pricing.** Cost is a floor; what to charge is commercial strategy.
- **Cloud run cost** → `finops-analyst`. **AI/token cost** → `ai-spend-report`.
  **Multi-year lifecycle cost** → `tco-model`. **Tracking against budget** → `budget-tracking`.
- **Vendor quote evaluation** for quotes it has not been given.
- **Story points or velocity forecasting.** Different instrument, different failure modes.

## References

- `references/wbs-checklist.md` — decomposition prompts and the routinely omitted work
- `references/pert-math.md` — derivations, correlation, the normal-approximation caveat, worked example
- `references/reference-class.md` — building an outside view from this project's own history
- `references/templates/estimate-worksheet.csv` — spreadsheet-ready, formulas included
- `references/templates/estimate-rollup.md` — companion narrative template

## Interop

If `superpowers` is installed, use `superpowers:brainstorming` for step 2 and
`superpowers:verification-before-completion` before declaring the estimate final. If it is
not installed, run the exit-criteria checklist manually and say that you did.

Record the realised uplift factor, the agreed rate basis and the contingency policy with
`memory_write` as facts of type `metric` or `decision` — that is what builds the reference
class for the next estimate. Never edit files under `.foundry/memory/` by hand.
