---
name: tco-model
description: Build a multi-year total cost of ownership model covering build, run, maintain and decommission over a stated horizon, with discounting and the cost lines teams routinely forget — observability, backups, egress, on-call, licences, certificate and dependency upkeep, and decommissioning. Use for build-vs-buy decisions, vendor comparisons, architecture choices with different run-cost profiles, and any time someone quotes a build cost as if it were the cost.
user-invocable: true
argument-hint: "[system or option name] [--horizon 5] [--rate 0.08]"
agent: foundry-economics:cost-engineer
model: opus
effort: high
metadata:
  foundry.vertical: economics
  foundry.io: "estimate.v1 -> estimate.v1"
license: Apache-2.0
---

# Total cost of ownership model

A build cost is not a cost. It is the **first instalment**. This skill produces a model of the
whole horizon so that a build-vs-buy or architecture decision is made on the number that will
actually be paid.

**Not financial advice.** Analytical decision support only.

## Provenance rule

`[measured: <path>]`, `[given: <who/when>]` or `[ASSUMPTION — confirm]` on every figure.
Placeholders look like placeholders: `<<TBC: annual licence, EUR>>`. Never invent a vendor
price, a cloud rate or a headcount cost. A TCO model with visible holes drives the right
conversation; one with invented numbers drives the wrong decision confidently.

## Step 1 — Fix the frame before any number

These four decisions determine the answer more than any cost line. Get them agreed and written
down first, because changing them later invalidates everything.

| Decision | Guidance |
|---|---|
| **Horizon N** | Match the expected useful life, not the budget cycle. Too short flatters build-your-own; too long flatters buy. State it in the title of every output. |
| **Discount rate r** | State it and its basis. `r = 0` is a claim that money next year equals money today — if you use it, say you are, and say why. |
| **Boundary** | What is inside the system? Shared platform, shared team, shared observability stack — allocated or excluded? Write the rule down. |
| **Comparability** | If comparing options, they must deliver the **same outcome**. A cheaper option that does less is not cheaper; normalise the scope first or the comparison is void. |

## Step 2 — Populate the four cost blocks

Open `references/cost-lines.md` and walk every section. It is deliberately long: the value of
a TCO model lies almost entirely in the lines nobody remembered.

```
C_t = build_t + run_t + maintain_t + decommission_t
```

- **build** — from the `estimate-project` skill. Do not re-estimate it here; read the
  `estimate.v1` artifact with `blackboard_read`.
- **run** — infrastructure, licences, third-party APIs, support and on-call, AI/token spend.
  Delegate cloud lines to `finops-analyst` and AI lines to `ai-spend-report` rather than
  guessing them.
- **maintain** — dependency upgrades, security patching, platform version migrations,
  regression suite upkeep, certificate and key rotation, drift repair.
- **decommission** — data export and archive retention, contract exit, user migration,
  the final decommissioning project itself.

Fill `.foundry/economics/tco-model.csv` from
`references/templates/tco-model.csv`. Keep one row per cost line per year; roll up with
formulas, never by hand.

## Step 3 — Model the shape, not just the total

Cost lines have shapes. Getting the shape wrong is worse than getting the level wrong, because
the shape drives cash flow and the go/no-go month.

| Shape | Examples | Modelling note |
|---|---|---|
| One-off, year 0 | Build, migration, initial licences | Watch for a second one-off in a later year (platform upgrade) |
| Flat recurring | Licences per seat, support contract | Check the contractual uplift clause — many index annually |
| Volume-scaling | Cloud compute, egress, per-transaction fees, tokens | Needs a volume forecast; make it an explicit driver row |
| Step function | An extra environment, a support tier, a new region, an extra FTE | The step is where budgets break. Show the trigger volume. |
| Rising | Technical-debt servicing, dependency upkeep on an ageing stack | Do not model as flat; state the growth assumption |
| Terminal | Decommissioning, contract exit fees, data egress on exit | Lands in year N and is almost always omitted |

Where a line scales, model it as `driver × unit rate` with the driver on its own row, so the
whole model re-runs when the volume forecast changes.

## Step 4 — Discount

```
PV(C_t) = C_t / (1 + r)^t
TCO     = Σ_{t=0..N} C_t / (1 + r)^t
```

Also report the **undiscounted** total. Non-financial stakeholders reason in cash-out terms and
will otherwise mistrust the number; showing both costs nothing and buys credibility.

Convention discipline: nominal cash flows need a nominal rate; real cash flows need a real
rate. If you inflate cost lines, you are in nominal terms. Mixing the two is a common and
material error — state which convention you used. Full treatment in `references/discounting.md`.

Equivalent annual cost, when comparing options with **different lifetimes**:

```
EAC = TCO / annuity_factor,    annuity_factor = (1 − (1+r)^(−N)) / r
```

Comparing a 3-year option against a 7-year option on raw TCO is meaningless. EAC is the
correct comparator.

## Step 5 — Sensitivity and the crossover

A TCO model that outputs one number has wasted the model. Report:

- **One-way sensitivity** on the top drivers: which single line moves the total most?
- **The crossover** when comparing options: at what volume, horizon or price does the ranking
  flip? `<<TBC: "buy wins below X requests/month; build wins above">>` is far more useful than
  a winner, because the volume forecast is the least reliable input in the model.
- **Horizon sensitivity**: re-run at N−2 and N+2. If the recommendation flips, the decision is
  really a bet on the system's lifetime — say so explicitly.

## Step 6 — Emit the artifact

Write via `blackboard_write`:

```
wave:   tco
agent:  cost-engineer
schema: estimate.v1
```

- One item per major cost block per year, `unit: "eur"`, with `optimistic`/`likely`/`pessimistic`
  — a multi-year run cost is genuinely a range.
- `scope` carries the frame: `"TCO, <system>, N=5 years, r=<<TBC>>, boundary: <…>"`.
  The schema is `additionalProperties: false`, so horizon and rate live in `scope`, not in
  fields of their own.
- `assumptions[0]` states the horizon, the rate and its basis.
- `excluded[]` lists what is outside the boundary. Mandatory.

Companion narrative from `references/templates/tco-summary.md`. Return only paths plus
≤ 300 tokens.

## Exit criteria

- [ ] Horizon, discount rate and its basis, and the boundary rule all stated
- [ ] Options normalised to the same delivered outcome before comparison
- [ ] Every section of `references/cost-lines.md` walked; deliberate omissions recorded
- [ ] Each line has a shape (one-off / flat / scaling / step / rising / terminal)
- [ ] Every scaling line has an explicit driver row
- [ ] Decommissioning costed and non-zero, or its zero explicitly justified
- [ ] Discounted **and** undiscounted totals reported
- [ ] EAC reported when option lifetimes differ
- [ ] Crossover point identified when comparing options
- [ ] Horizon sensitivity run at N−2 and N+2
- [ ] Zero unlabelled numbers
- [ ] `blackboard_write` returned VALID

## What this skill deliberately does not cover

- **Benefits and revenue.** This is the cost side only. Net value, NPV and payback →
  `business-plan`.
- **Build effort estimation** → `estimate-project`. This skill consumes that estimate.
- **Cloud rate optimisation and commitments** → `finops-analyst`.
- **AI/token spend detail** → `ai-spend-report`.
- **Accounting treatment**: capex vs opex classification, capitalisation of development,
  depreciation schedules for statutory purposes, lease accounting. Where the model uses a
  depreciation profile it is a modelling convention, flagged as such, not an accounting policy.
- **Vendor negotiation** and contract terms.
- **Carbon or energy accounting.**
- **Risk-adjusted simulation.** Deterministic scenarios only; a Monte Carlo over invented
  distributions adds precision, not information.

## References

- `references/cost-lines.md` — the full checklist, including the forgotten lines
- `references/discounting.md` — discounting, EAC, nominal vs real, the r=0 trap
- `references/templates/tco-model.csv` — spreadsheet-ready, formulas included
- `references/templates/tco-summary.md` — decision-facing summary template

## Interop

Delegate rather than duplicate: `estimate-project` for build, `finops-analyst` for cloud run
cost, `ai-spend-report` for token spend, `funding-analyst` if any of it is grant-eligible.

Record the agreed horizon, discount rate and boundary rule with `memory_write` as facts of
type `decision` — they will otherwise be silently redefined in the next comparison, which is
the classic way two TCO models of the same system disagree.
