---
name: commitment-coverage
description: "Commitment coverage, utilisation, expiry exposure and break-even from a billing export (the rate half)."
kind: skill
pack: finops
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: commitment-coverage

## Premise

Commitments are the one cost lever that changes the bill without changing the architecture — and the one most often bought on intuition. Two numbers decide everything, and they pull in opposite directions: **coverage** (how much eligible usage receives a discount) and **utilisation** (how much of what was bought is actually consumed). Maximising either alone is a mistake; 100% coverage means over-buying, and 100% utilisation usually means under-buying.

Every figure comes from the provider's own coverage and utilisation reporting plus the cost/usage export. No modelled assumptions about future usage without labelling them.

## The bill lane — `bill-lane.py commitments`

The inventory and its expiry calendar are read with the pack's stdlib script (`.claude/skills/unit-cost-probe/scripts/bill-lane.py`, shipped with `unit-cost-probe`; `--self-test` first): `columns <export>` names the cost column, then `commitments <export> --period YYYY-MM` prints coverage per currency (commitment-covered usage cost ÷ eligible usage cost) and, per FOCUS `CommitmentDiscountId`, the used and unused cost and the utilisation from `CommitmentDiscountStatus`; `--expiry <inventory> --as-of <date> --within-days 90` joins the end dates (exports rarely carry them) and flags what expires inside the window. The floor (step 4) still needs hourly usage over a seasonal cycle — the script reads cost rows, not hours. Commitments are bought in a billing console, never in Terraform: this skill never runs because an IaC root exists, only on an export or an inventory the user supplies.

### The ledger line (UE-3)

Every run, including one that halts, ends with one line an audit ledger can print unchanged:

```
UE-3 commitment-coverage · checked (<n> commitments, coverage <%>, utilisation <%>, <k> expiring ≤ 90 d)
UE-3 commitment-coverage · NOT-RUN (no billing export | no commitment inventory)
UE-3 commitment-coverage · blocked (<the halt below>)
UE-3 commitment-coverage · N/A (flat-rate capacity | provider offers no commitment for this usage)
```

A recommendation is a bet, not a finding; an expiring commitment with no owned notification is a guardrail gap that `/cost-guardrails` installs (class 6). Numbers here are reconciled by V589's arithmetic ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § FinOps) and read against [`precedents/finops.md`](../../../../snippets/precedents/finops.md) § 4 (commitments already paid change the sign of a downsizing) before any `/cost-review` row cites them.

## Halt conditions

Each halt prints its ledger line (above) and stops.

- **Baseline usage undetermined** — a commitment is a bet on a floor. Without at least a full seasonal cycle of usage history, the floor is a guess; say so rather than recommending a term.
- **Planned architectural change undisclosed** — a migration, a re-platform, or a major shape change inside the commitment term invalidates the arithmetic. Ask before recommending.
- **Term and payment options unknown** for the provider and account in question.
- **Existing commitment inventory unavailable** — you cannot recommend a purchase without knowing what is already owned and when it expires.
- **Flat-rate capacity environment** — commitments may not apply at all. Confirm the model first.

## When to run

- Before any commitment purchase or renewal.
- Quarterly, as a standing review.
- Before a capacity change large enough to move the baseline.
- When an expiry is inside the next two months — an expiring commitment is a scheduled bill increase that surprises people every time.
- When `@finops-analyst` classifies a spend delta as a **rate** change.

## Procedure

### 1. Inventory what is owned

Per commitment: type, scope (account / shared / service-specific), term, payment option, hourly or monthly value, start and expiry, and current utilisation. Sort by expiry.

### 2. Measure coverage

```
coverage = eligible usage covered by a commitment / total eligible usage
```

Compute per service and per commitment scope, not just in aggregate — aggregate coverage hides a fully-covered service subsidising an uncovered one.

Note explicitly what is *not eligible*: usage types that no commitment covers. Chasing coverage on ineligible usage is a common and expensive misunderstanding.

### 3. Measure utilisation

```
utilisation = commitment value consumed / commitment value purchased
```

Under-utilisation is money already spent for nothing. Report per commitment, with the wasted amount per period in currency, not just a percentage.

### 4. Find the floor

The purchase decision rests on the **sustained minimum** — usage that is present in essentially every hour of the trailing period, not the average. Compute a low percentile of hourly usage over a full seasonal cycle, and commit at or below it. Committing at the average guarantees under-utilisation during troughs.

State the floor, the percentile used, and the window. Then state how much of the floor is *durable*: usage attached to a workload with a known end date, or a system scheduled for migration, is not a floor.

### 5. Break-even

For each recommendation, compute the break-even point: at the discount rate offered, what fraction of the term must the usage persist for the commitment to beat on-demand? Compare that against the confidence in the workload's lifetime.

A commitment is a bet. State the bet: *"this saves X if usage stays above Y for Z months; it loses if the workload is retired before month N."*

### 6. Recommend

One of: **buy** (with type, scope, term, payment option, and quantity), **hold** (coverage adequate; state the number), **partial** (cover the durable floor only), or **let lapse** (with the resulting bill increase stated, so it is a decision rather than a surprise).

#### Which instrument: read the denomination, not the discount

"Prefer flexible over rigid" is unactionable until you name what makes one flexible. The axis is **what the commitment is denominated in**, and it is the same axis on every provider even though the product names differ:

| Denominated in | Floats across | Strands when | Discount |
|---|---|---|---|
| **spend per hour** (a currency rate) | shape, size, family, often region and even service | you stop spending that much at all | lower |
| **a resource quantity** (vCPU + memory, capacity units, nodes) | size within a family, sometimes region | you change family or region | middle |
| **a specific shape** (this instance type, this configuration, this region) | almost nothing | any routine re-shaping | highest |

The decision rule follows directly, and it is about the *system*, not about the discount table: **commit at the coarsest denomination whose floor you are confident in.** A spend-denominated commitment survives a migration you have not planned yet; a shape-denominated one is a bet that the shape outlives the term. In a system still changing shape, the difference between the two discounts is the price of an option, and that option is frequently worth more than the spread.

Name the instrument in the **provider's own product name** in the report — "1-year no-upfront compute spend commitment" is what the finance team can act on; "flexible instrument" is not, and it cannot be looked up. Where a project's export conforms to FOCUS (see `STACK.md`), `Commitment Discount ID` and `Commitment Discount Status` are where the inventory and its state actually live, and the status column is what makes step 1's expiry sort reproducible rather than manual.

Two failure modes this axis exposes that a discount comparison never will: a commitment bought one denomination too narrow for a system that re-shapes routinely (strands on the next family change), and one bought too coarse for a workload with a genuinely fixed shape (pays for flexibility it will never exercise).

### 7. Report

```
## commitment-coverage — <account/scope> — <date>

### Inventory (by expiry)
| Commitment | Provider's product name | Denominated in | Scope | Term | Value/hr | Expiry | Utilisation | Wasted/period |

### Coverage
| Service | Eligible usage | Covered | Coverage % | Ineligible usage (no commitment applies) |

Aggregate coverage: <%>   Aggregate utilisation: <%>

### Floor
Sustained minimum: <value> (p<n> of hourly usage over <window>)
Durable share:     <value> (excluding <named workload> — <reason>)

### Recommendation
Action: buy | hold | partial | let lapse
  <provider's product name, denomination, scope, term, payment option, quantity>
Break-even: usage must persist <n> of <term> months
The bet:    saves <$> if <condition>; loses <$> if <condition>
Expiry exposure (next 90d): <$/month increase when <commitment> lapses>
```

## Inputs

- The provider's coverage and utilisation reporting.
- Hourly usage history over a full seasonal cycle.
- The current commitment inventory with expiry dates.
- Known upcoming architectural changes.

## Outputs

- The report block above.
- An expiry calendar for `/cost-guardrails` — every expiry becomes a scheduled notification with an owner, so a lapse is a decision rather than an invoice surprise.
- The rate-change explanation for `@finops-analyst`'s delta analysis.

## False positives / gotchas

- **Optimising coverage alone.** 100% coverage with 60% utilisation is worse than 70% coverage with 95% utilisation.
- **Committing at the average.** The average is above the floor by construction; the trough hours are unutilised.
- **Ignoring the seasonal cycle.** A commitment sized on a peak quarter under-utilises for the other three.
- **Missing scope rules.** Commitments differ sharply in what they can float across (accounts, families, regions, sizes); a commitment bought at the wrong scope can strand.
- **Comparing two instruments on discount alone** when they are denominated differently. That comparison is not like-for-like — one of them is also selling an option on the system's future shape, and the spread is its price.
- **Double-counting a discount** that a provider already applies automatically at the organisation level.
- **Recommending a long term for a workload with a shorter roadmap** — the break-even calculation exists to make that visible.
- **Reading utilisation as of today** on a commitment purchased last week; it has not had time to be representative.
- **Treating an expiry as a renewal.** It is a decision point, and the default outcome is a bill increase.

## Related

### Skills
- `unit-cost-probe` — a commitment changes the numerator, so unit costs shift for rate reasons; keep the two explanations separate.
- `spend-anomaly-triage` — a commitment expiry is a common cause of an apparent anomaly with no usage change.

### Agents
- `@finops-analyst` — supplies the usage history and classifies rate changes.
- `@cost-architect` — a design that is about to change shape invalidates a long commitment; run them together.

### Commands
- `/cost-guardrails` — receives the expiry calendar.
- `/cost-model` — commitment amortisation is what makes its branches honest.

### Patterns
- `ai/patterns/commitment-strategy.md`, `ai/patterns/unit-economics.md`
