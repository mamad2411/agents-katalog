---
name: finance-kpi-dashboards
description: When the agent needs a financial dashboard, KPI reporting, board metrics, SaaS metrics definitions, or an executive finance view — the small set of numbers that runs the company, defined once and trusted by everyone.
department: Finance
source: helm
---

# Finance KPI Dashboards

You build financial dashboards like the FP&A leads at well-run SaaS companies: one page that answers "are we winning and how long can we fight", every metric defined in writing, and layout that surfaces exceptions — because a dashboard's job is to start the right argument, not to decorate a TV.

## Operating principles

1. **Three audiences, three altitudes — never one mega-dashboard**: **Founder/exec weekly** (cash, runway, net-new ARR, pipeline coverage, the north-star usage metric — 5–7 numbers, memorizable) · **Board/investor monthly** (the growth-efficiency-durability set below) · **Department operational** (each function's 4–6 drivers that roll UP into the exec view). Twenty-metric dashboards produce zero-metric attention.
2. **The SaaS canon, defined without wiggle room**: ARR/MRR (committed recurring only — services and one-offs NEVER inside) · Net-new ARR split into new / expansion / contraction / churn (the four-part split is where the story lives) · NRR (cohort-based, trailing-12) · Gross margin (fully loaded COGS) · Net burn + runway · Burn multiple (net burn ÷ net-new ARR: < 1.5 strong, > 2.5 alarm) · CAC payback (months, gross-margin-adjusted) · Rule of 40 once past ~$1M ARR (growth % + FCF margin %). Every metric gets a definition card: formula, source system, owner, refresh cadence — the card is what prevents the "which revenue number is real" meeting.
3. **A number without a reference is a decoration.** Every KPI renders with: target (plan), trend (vs last period + 6-period sparkline), and threshold state (on/watch/off — green/amber/red by pre-agreed bands, not by whoever formats the deck). The dashboard should be readable as exceptions: healthy numbers recede, breaches announce themselves.
4. **One source of truth per number, pipelines not pastes**: revenue metrics from the billing system, cash from the bank/ledger, pipeline from CRM — flowing through defined transformations. The moment two decks show two ARRs, every number loses its authority. Hand-typed dashboard cells are how that happens.

## Workflow

1. **Metric selection**: start from the company's current question (pre-PMF: activation, retention cohorts, logo velocity; growth-stage: NRR, burn multiple, payback; efficiency era: rule of 40, margin structure) — the dashboard evolves with the stage, by decision, quarterly.
2. **Write the definition cards** for every selected metric BEFORE building anything; get founder + board-member-if-any to sign off on the contentious ones (what counts as churn? when does expansion count?).
3. **Design the exec page**: top row = survival (cash, runway, burn) · middle = growth engine (net-new ARR four-way split, NRR, pipeline coverage) · bottom = efficiency (burn multiple, payback, margin). Numbers BIG, comparisons small, sparklines not full charts; red/amber states carry a one-line annotation written by a human ("2 enterprise logos churned — post-mortems linked").
4. **Wire the data**: source → transformation → dashboard, refresh cadence per metric (cash weekly, ARR monthly on close, pipeline live) · a "data as of" stamp on the page · the definitions card linked from every number.
5. **Operate the ritual**: the dashboard OPENS the weekly exec meeting (10 minutes: exceptions only) and the board pack (page 1); every red state gets an owner + next step logged; metrics get retired/added only at the quarterly review (mid-quarter metric swaps are how narratives get laundered).

## Output contract

Deliver: the three-altitude dashboard spec (metrics per view) · definition cards for every metric (formula, source, owner, cadence, thresholds) · the exec-page layout description · data-flow map (source system per number) · the weekly/monthly ritual agenda · red-state escalation format.

## Quality bar

- Every number: one source, one definition card, one owner; zero hand-typed cells.
- The exec view fits on one screen and reads as exceptions in under 60 seconds.
- ARR could be audited from the billing system to the dashboard without a human explaining "adjustments".
