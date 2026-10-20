---
name: budget-tracking
description: Set up and run budget-versus-actual tracking with earned-value variance analysis, forecast at completion, and an agreed escalation threshold. Use when a project has a budget and someone must know whether it will hold, when a monthly cost review is due, when a variance needs explaining, or when a re-baseline is being proposed. Turns a one-off estimate into a control instrument.
user-invocable: true
argument-hint: "[setup|review] [--period YYYY-MM]"
agent: foundry-economics:cost-engineer
model: opus
effort: high
metadata:
  foundry.vertical: economics
  foundry.io: "estimate.v1 -> estimate.v1 + risk.v1"
license: Apache-2.0
---

# Budget tracking

An estimate that is never compared to reality is a guess nobody learned from. This skill makes
the estimate a **control instrument**: measured every period, with a variance explanation, a
forecast, and a pre-agreed threshold at which someone is told.

**Not financial advice.** Analytical decision support, not statutory reporting.

## Two modes

`setup` — establish the baseline and the control loop. Run once, before spending starts.
`review` — run the loop for one period. Run on a fixed cadence, not when someone is worried.

---

# Mode: setup

## S1 — Freeze the baseline

The baseline is the `estimate.v1` that was **approved**, not the latest one. Read it with
`blackboard_read`. Record which artifact and which date, because "the budget" will otherwise
drift silently into meaning "the current forecast", which destroys the whole measurement.

```
BAC = budget at completion = approved total, including agreed contingency
```

State whether contingency is inside BAC or held separately by the sponsor. This one decision
determines whether the project looks over budget the first time a risk materialises — get it
agreed in writing rather than discovering the disagreement during a variance review.

## S2 — Build the time-phased plan

A budget without a time phasing cannot produce a schedule variance, so half the diagnosis is
unavailable.

```
PV_t = planned value = budget planned to be earned by end of period t
```

Phase by the plan's own waves and tasks (`plan.v1`), not by dividing the total by the number
of months. Straight-lining is the most common shortcut here and it makes every early period
look ahead of schedule.

## S3 — Define how "earned" is measured

This is the decision that makes or breaks earned value. Choose per work package and write it
down:

| Rule | Earn | Use for |
|---|---|---|
| 0/100 | nothing until done, then all | short packages; the most honest default |
| 50/50 | half at start, half at completion | medium packages |
| Milestone-weighted | at defined verifiable milestones | long packages with real checkpoints |
| Units complete | proportional to countable deliverables | repetitive work |
| **Percent complete (subjective)** | whatever someone says | **avoid** — it is the mechanism by which projects are 90% complete for months |

## S4 — Set the escalation thresholds

Write them to `.foundry/economics/budget.json` (schema in `references/budget-config.md`). Agree
them **before** the first variance, when nobody is defending anything:

| Level | Typical trigger | Action | Who |
|---|---|---|---|
| Green | within threshold | note it in the period report | project lead |
| Amber | `CPI < <<TBC>>` or `VAC > <<TBC>>%` of BAC | written explanation + recovery action with a date | project lead → sponsor |
| Red | `CPI < <<TBC>>` or forecast breach of BAC | stop-and-decide: re-baseline, de-scope, or fund | sponsor |

Thresholds are `[given]` by the sponsor. Do not invent them; propose them and get them agreed.

## S5 — Wire up the actuals

`AC` must come from a system of record, not from memory. Name the source per cost category —
timesheets, purchase ledger, cloud billing export, `ai-spend-report` — and the cut-off day of
the period. An actual whose source is not named is not an actual.

Set the cadence: monthly is the default; weekly for short or high-burn projects. **Fixed
cadence, not on-demand** — a review that only happens when someone is worried is a review that
systematically misses the early signal.

---

# Mode: review

## R1 — Collect three numbers per work package

```
PV  planned value   — from the time-phased baseline
EV  earned value    — from the S3 rule, not from an opinion
AC  actual cost     — from the system of record named in S5
```

Fill `.foundry/economics/budget-vs-actual.csv` from
`references/templates/budget-vs-actual.csv`.

## R2 — Compute

```
CV   = EV − AC                    cost variance      (negative = over budget)
SV   = EV − PV                    schedule variance  (negative = behind)
CPI  = EV / AC                    cost performance index
SPI  = EV / PV                    schedule performance index
EAC  = BAC / CPI                  forecast at completion, if current efficiency persists
ETC  = EAC − AC                   estimate to complete
VAC  = BAC − EAC                  variance at completion
TCPI = (BAC − EV) / (BAC − AC)    efficiency the remaining work must achieve
```

Concepts from earned value management (ANSI/EIA-748; summarised in the PMBOK Guide).

**The TCPI test is the honest one.** If `CPI < 0.9` and `TCPI > 1.1`, the plan requires an
efficiency the team has never demonstrated. Say that plainly. Reporting a green EAC on the
strength of a recovery nobody has evidence for is the most common way a budget failure becomes
a surprise. Alternative EAC formulas and when each applies: `references/evm.md`.

## R3 — Explain each variance

A number without a cause is not a variance analysis. For each package outside threshold, state:

1. **Cause** — price, quantity, scope, productivity, or timing? These have different fixes.
   `price variance = (actual rate − planned rate) × actual quantity`
   `quantity variance = (actual qty − planned qty) × planned rate`
2. **Permanent or timing?** A timing variance reverses; a permanent one does not. Do not report
   a timing variance as an overrun, and do not report an overrun as timing because you hope so.
3. **Trend** — one period or three? A single period is noise. Three in the same direction is a
   trend and needs a decision.
4. **Action** — what changes, who owns it, by when, and what will prove it worked.

Method and the diagnostic tree: `references/variance-analysis.md`.

## R4 — Update the risk register

Materialised risks move to actuals and reduce remaining contingency. Report:

```
contingency drawn to date / contingency remaining / Σ exposure of open risks
```

If open exposure exceeds remaining contingency, the budget is already in deficit in expectation
even when the actuals look green. **This is the earliest available signal and the one most
often missed** — surface it every period, in the headline, not in an annex.

## R5 — Report and escalate

Render `references/templates/variance-report.md`. Emit an updated `estimate.v1` (wave
`budget-review`, `scope` naming the period) via `blackboard_write`, and a `risk.v1` for any
forecast breach with `category: "cost"`, an `owner` and a `reviewBy` date.

Escalate strictly per the S4 thresholds. Thresholds exist so escalation is not a judgement
call made by the person with the most to lose from escalating.

## R6 — Re-baseline only deliberately

Re-baselining resets the variance to zero and erases the record of how the overrun happened.
It is legitimate for an **approved scope change**. It is not legitimate as a way to make a red
report green.

If you re-baseline: record the old BAC, the new BAC, the reason, the approver and the date, and
**keep reporting against the original baseline in parallel** for the rest of the project. A
project that has been re-baselined three times with no memory of the original number has no
budget at all.

## R7 — Bank the outcome

At completion, record the actual-versus-estimate outcome with `memory_write` as a fact of type
`metric`, including which *category* of work was underestimated. That is the raw material for
the reference-class check in `estimate-project`. Skipping it guarantees the next estimate
repeats the same omission.

---

## Exit criteria

**Setup:** baseline artifact and date recorded · contingency treatment agreed in writing ·
time-phased PV from the plan, not straight-lined · an earning rule written per work package,
none of them subjective percent-complete · thresholds in `.foundry/economics/budget.json`,
`[given]` by the sponsor · actual source named per category with a cut-off day · cadence fixed.

**Review:** PV, EV, AC present for every package · CV, SV, CPI, SPI, EAC, ETC, VAC, TCPI
computed · **TCPI test performed and stated** · every out-of-threshold variance has cause,
permanent-or-timing, trend and an owned action with a date · contingency drawn vs remaining vs
open exposure reported in the headline · escalation applied per threshold, not per judgement ·
any re-baseline documented with old BAC, new BAC, reason and approver · zero unlabelled
numbers · `blackboard_write` returned VALID.

## What this skill deliberately does not cover

- **Statutory or management accounting.** Not a general ledger, not month-end close, not
  accruals, not audit. Figures here are for control, not for filing.
- **Schedule management.** No critical path, no resource levelling. SPI is a cost-based proxy
  for schedule and a poor one near the end of a project — it converges to 1.0 as work
  completes regardless of lateness. Say so when you report it late in a project.
- **Timesheet approval or payroll.** It consumes timesheet data; it does not manage it.
  Grant-compliant timesheets → `funding-analyst`.
- **Procurement and invoice approval.**
- **Producing the original estimate** → `estimate-project`. **Lifecycle cost** → `tco-model`.
  **Whether the project is still worth doing** → `business-plan`.
- **Individual performance measurement.** EVM measures work packages, not people. Refuse to
  produce per-person variance.

## References

- `references/evm.md` — formulas, EAC variants and when each applies, the limits of EVM
- `references/variance-analysis.md` — the diagnostic tree and how to write a variance narrative
- `references/budget-config.md` — `.foundry/economics/budget.json` schema
- `references/templates/budget-vs-actual.csv` — spreadsheet-ready, formulas included
- `references/templates/variance-report.md` — period report template

## Interop

If `superpowers` is installed, use `superpowers:verification-before-completion` before
declaring a period green; otherwise run the exit criteria manually. Record threshold decisions
and re-baselines with `memory_write` as facts of type `decision`; a re-baseline that is not in
project memory will be forgotten by the next review, which is exactly how a budget quietly
stops existing.
