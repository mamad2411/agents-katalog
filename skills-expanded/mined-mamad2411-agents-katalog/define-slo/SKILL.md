---
name: define-slo
description: Turn one user journey into SLIs, an SLO with a justified target, an error-budget policy with real consequences, and multi-window multi-burn-rate alerts. Use when reliability is discussed without numbers, before promising an availability figure, when alerts are noisy or ignored, or when an SLA is being drafted. Produces docs/slo/<journey>.md plus alert definitions and runbook stubs. Do not use for component-level SLOs nobody's journey depends on.
allowed-tools: Read Grep Glob Bash Write Edit
argument-hint: "[journey-name] [--window 28]"
user-invocable: true
model: opus
effort: high
metadata:
  foundry.vertical: quality
  foundry.io: "requirement.v1 -> plan.v1 + docs/slo/<journey>.md"
license: Apache-2.0
---

# Define an SLO for a user journey

One journey at a time. The output is a document a product manager can read and an alert an
on-call engineer will believe.

Two positions held throughout: **100% is the wrong target**, and **an SLO with no consequence is
decoration**.

## When not to use this

- The component has no user journey depending on it → an SLO on it will not tell you whether
  anyone is having a bad time. Use RED metrics and a dashboard instead.
- You have no measurement of current behaviour → step 2 will stop you. Measure for 28 days
  first; publish an "aspiration" clearly labelled as not an SLO if something must be said now.
- You need a CI performance gate → `perf-budget`. Different instrument, different consequence.
- The organisation will not accept any consequence for exhausting the budget → ship the
  measurement and the alerts, mark the policy blocked, and name the decision-maker. Do not
  write a policy you know is unenforced.

## Step 1 — State the journey as a user would

> "I can place an order and see it confirmed."

Not "the orders service is up". If you cannot write the sentence in the user's voice, you are
about to write a component SLO.

Then list the **critical operations** that must work for that sentence to be true, and the
**business consequence** when it is false (lost revenue per hour, support contacts, churn,
regulatory exposure). Without the consequence you cannot justify a target and the conversation
becomes taste.

## Step 2 — Specify the SLI

Every SLI is a ratio. Write down all four decisions; each ambiguity here becomes an argument at
03:00.

```
SLI = good events / valid events
```

| Decision | Example | Trap it avoids |
|---|---|---|
| What is an event? | one HTTP request to `POST /orders` | counting retries as separate user experiences |
| What makes it good? | `status < 500 AND duration <= 800ms` | a 30-second success counted as good |
| What is valid? | excludes health checks, synthetic probes, and 400s caused by malformed client input | excluding away your own failures |
| Where measured? | load balancer access logs | application metrics miss requests that never arrived |

Measurement point, in order of preference: **client/RUM > CDN/edge > load balancer >
application**. Every step down the list makes a class of real outage invisible; name which class
you have accepted.

**Latency SLIs are threshold ratios, not percentiles.** "99% of requests under 800 ms" aggregates
correctly across instances and composes with an error budget; "p99 ≤ 800 ms" does neither
reliably. Prefer the ratio form.

Every exclusion from `valid` is listed and defended in the document. Exclusions are where SLOs go
to become meaningless.

Write the query that computes it, and run it:

```bash
# Example against structured access logs - adapt to your backend, but RUN it before publishing
node -e '
const fs=require("node:fs");
let good=0,valid=0;
for(const line of fs.readFileSync(process.argv[1],"utf8").split("\n")){
  if(!line.trim())continue; let e; try{e=JSON.parse(line)}catch{continue}
  if(e.path!=="/orders"||e.method!=="POST")continue;
  if(e.user_agent==="health-check")continue;              // documented exclusion
  if(e.status>=400&&e.status<500)continue;                // documented exclusion: client-caused
  valid++; if(e.status<500&&e.duration_ms<=800)good++;
}
console.log(JSON.stringify({good,valid,sliPercent:+(100*good/valid).toFixed(3)}));
' access.jsonl
```

## Step 3 — Justify the target

Three inputs. Refuse to set a target without all three.

1. **Measured baseline over ≥ 28 days.** Compute it with the query above.
2. **The point where users actually complain or leave.** Support tickets correlated with the
   SLI, churn analysis, or a product decision written down and attributed to a person.
3. **The cost of the next nine** in money or engineering months: redundancy, multi-region,
   slower release cadence, larger on-call rota.

Set the target **slightly below** honest current performance when users are content — that is
what creates budget to spend on shipping. Set it higher only with evidence of harm, and pair it
with the funded work.

Error budget per 28-day window (`40320 minutes x (1 - target)` — verify the arithmetic yourself):

| SLO | Budget per 28 days |
|---|---|
| 99% | 6 h 43 m |
| 99.5% | 3 h 22 m |
| 99.9% | 40 m 19 s |
| 99.95% | 20 m 10 s |
| 99.99% | 4 m 2 s |

Three checks that kill most proposed targets:

- **Dependency floor.** You cannot promise more than your hard dependencies deliver unless you
  can operate without them. Compute the serial composition (multiply the availabilities) and
  show it. A journey over three dependencies at 99.9% each has a 99.7% ceiling before your own
  code contributes a single failure.
- **Deploy cost.** 40 deploys a month with a 30-second blip each is 20 minutes — half of a
  99.9% budget spent on shipping, before anything breaks.
- **Human response time.** At 99.99% you have 4 minutes a month. You cannot page a human into
  that. Any target at or above 99.99% requires automated mitigation and you must say so.

## Step 4 — Error-budget policy with consequences

Write it before the budget is spent. After is a negotiation; before is a decision.

| Consumed | Consequence |
|---|---|
| < 50% | Normal operation; risky experiments affordable |
| 50–75% | Reliability work prioritised next cycle; top consumer reviewed |
| 75–100% | Non-essential feature deploys stop; postmortem actions take priority; a named person owns recovery |
| Exhausted | Freeze except reliability and security; lifts when the rolling 28-day window is back in budget — not on a calendar date |
| Exhausted twice in a quarter | Target renegotiated with the business, up or down |

Also required: an **exemption path** (who can override, how it is recorded). Without one, teams
route around the policy and you lose the signal instead of the freeze.

Start from `references/policy-template.md`.

Signed by a named engineering owner and a named product owner, with a date. Unsigned, it is a
wish.

## Step 5 — Burn-rate alerts

```
burn_rate = observed_error_ratio / (1 - target)
```

Burn rate 1 exhausts the budget exactly at the end of the window. Two-tier configuration for a
28-day window:

| Tier | Burn rate | Long window | Short window | Budget spent before firing | Action |
|---|---|---|---|---|---|
| Fast | 14.4x | 1 h | 5 m | ~2% | **Page** |
| Medium | 6x | 6 h | 30 m | ~5% | **Page** |
| Slow | 3x | 24 h | 2 h | ~11% | Ticket |
| Very slow | 1x | 72 h | 6 h | ~11% | Ticket |

The **short window is an AND condition** on the long window — it must also be burning right now.
Without it the alert keeps firing for hours after the incident is over and on-call silences it.
That pairing is the entire reason this design works.

Rules:
- Only fast and medium page. A slow burn is real but it is not a 03:00 problem.
- Every alert links a runbook at `.foundry/runbooks/<slug>.md` and names an owner.
- Do **not** add a raw-threshold alert on the same symptom "just in case" — duplicate alerting
  turns one incident into six pages.
- Recompute the windows if your SLO window is not 28 days. Do not copy the table blindly.
- Cap pages at **≤ 2 per 12-hour shift** sustained; above that, fix the service or fix the alert.

Worked derivations: `references/burn-rate-math.md`. Recording/alerting rule shapes:
`references/burn-rate-queries.md`. Check the arithmetic with the bundled calculator:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/slo-calc.mjs --target 99.9 --window 28
```

## Step 6 — Write the document

`docs/slo/<journey>.md`, with these sections in this order: journey sentence; SLI specification
(all four decisions); the query, with its last run and result; target with the three
justifications; dependency-floor arithmetic; error budget in minutes; the policy table with
signatures and dates; the alert definitions; runbook links; review date (**≤ 90 days**, since an
SLO that outlives its traffic assumptions misleads).

Emit the accompanying `plan.v1` to `.foundry/blackboard/<wave>/define-slo.json` with waves for
measurement, definition, alerting and policy sign-off, and `outOfScope` naming every journey
deliberately left without an SLO.

## Exit criteria

1. The journey is written in the user's voice, with a named business consequence.
2. All four SLI decisions are documented, and the exclusion list is enumerated and defended.
3. The SLI query has been **run** and its result recorded with a date.
4. The target cites a ≥ 28-day measured baseline, a user-harm point, and the cost of the next
   nine.
5. The dependency-composed floor is computed and shown; the target does not exceed it without a
   stated mitigation.
6. The error budget is stated in minutes and the arithmetic is shown.
7. The policy names consequences per band, has two named signatories with a date, and an
   exemption path.
8. Fast and medium burn-rate alerts are configured with paired short windows; each links a
   runbook and names an owner; no duplicate raw-threshold alert covers the same symptom.
9. A review date ≤ 90 days out is set.
10. The `plan.v1` artifact validates and `outOfScope` is non-empty.

## Degradation

- **No 28 days of data** → wave 1 is measurement; publish a clearly labelled aspiration, not an
  SLO, and do not alert on it.
- **Only application-side measurement** → state which failure classes are invisible (DNS, TLS,
  client network, total edge outage) and add a `medium` finding for external synthetic probes.
- **Single-person on-call** → targets above 99.9% are not deliverable. Say so plainly and record
  a `risk.v1` with an owner rather than writing an objective the rota cannot honour.
- **Alerting backend cannot express multi-window conditions** → implement the long window and add
  a manual resolve-check step in the runbook; record the reduced fidelity as a finding.
- **`superpowers` installed** → use `superpowers:brainstorming` to elicit journeys from
  stakeholders and `superpowers:writing-plans` to shape the waves. If absent, use
  `${CLAUDE_PLUGIN_ROOT}/references/tdd-fallback.md` §"Working without superpowers".

## Deliberately not covered

Instrumentation mechanics (`observability-engineer`), CI performance gates (`perf-budget`),
capacity planning (`performance-engineer`), contractual SLAs and penalties (legal vertical — this
skill supplies the SLO the SLA must sit safely behind, always with margin), and incident response
execution (`postmortem`, `sre-planner`).

## Bundled assets

- `scripts/slo-calc.mjs` — computes the error budget in failed events and downtime-equivalent
  minutes, the dependency ceiling, the 14.4/6/3/1 burn-rate table with trigger error rates and
  worst-case detection times, and flags alert windows that see too few events to be valid.
  Node.js >= 20, no dependencies, no clock read.
  `node scripts/slo-calc.mjs --target 99.9 --window 28 --rps 45 --deps 99.95,99.9,99.99`
  Exit code 1 means the target exceeds the dependency ceiling and is fiction.
- `references/burn-rate-math.md` — the arithmetic worked out.
- `references/burn-rate-queries.md` — recording and alerting rule shapes for a
  Prometheus-compatible backend, plus the nine ways this migration fails in practice.
- `references/policy-template.md` — the error-budget policy to fill in and have signed.
