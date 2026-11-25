---
name: spend-anomaly-triage
description: "Spend spike or creep to its cause: rate, usage and mix split, then a suspect ledger with a confirm test each."
kind: skill
pack: finops
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: spend-anomaly-triage

## Premise

A cost spike has a cause, and the cause is almost always something a human did on a specific day. The triage is a correlation problem with a small suspect list: deploys, feature-flag changes, traffic changes, scheduled jobs and backfills, commitment expiries, provider price changes, and incidents. The failure mode is stopping at "service X went up" — that is the observation, not the cause.

Every suspect carries a **confirm/refute test**: something cheap that would settle it. A suspect list with no tests is a list of theories.

## The bill lane — `bill-lane.py split`

The three-way split is computed, not estimated, with the pack's stdlib script (`.claude/skills/unit-cost-probe/scripts/bill-lane.py`, shipped with `unit-cost-probe`; `--self-test` first): `columns <export>` names the cost column, then `split <export> --base YYYY-MM --cur YYYY-MM --by sku|service` prints the rate, usage and mix parts per SKU or service and checks that they sum to the delta exactly (in `Decimal`, per currency). `summary <export> --by sku --period YYYY-MM` localises; a partial period is flagged, never compared as a whole one. The suspect correlation (deploys, flags, runs) stays this skill's reading.

### The ledger line (UE-4)

Every run, including one that halts, ends with one line an audit ledger can print unchanged:

```
UE-4 spend-anomaly-triage · checked (Δ <amount> <currency> = rate <…> + usage <…> + mix <…>; cause CONFIRMED | CORRELATED, UNCONFIRMED | UNKNOWN)
UE-4 spend-anomaly-triage · NOT-RUN (no billing export | no daily granularity)
UE-4 spend-anomaly-triage · blocked (<the halt below>)
```

A cause is a finding only after its confirm test ran; a correlated suspect is `Unconfirmed` with that test named, per [`refute-before-report.md`](../../../../snippets/refute-before-report.md) and [`precedents/finops.md`](../../../../snippets/precedents/finops.md) (§ 4, § 7). The split's arithmetic is V589's reconciliation ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § FinOps).

## Halt conditions

Each halt prints its ledger line (above) and stops.

- **Daily granularity unavailable.** Monthly figures cannot be correlated with a deploy. Get daily (ideally hourly) cost data or say the anomaly is not triageable at this granularity.
- **Change log unavailable** — no deploy history, no flag-change history. Say so; the correlation half of the method is unavailable and the output is a mechanism hypothesis at best.
- **The "anomaly" is a billing artefact** — an unamortised upfront purchase, a support fee, a credit expiring, a period boundary. Check these first, always; they explain a surprising share of apparent spikes and cost nothing to rule out.
- **Baseline never declared.** If no expectation existed, this is not an anomaly, it is a discovery. Say which — the follow-up actions differ.

## When to run

- A cost anomaly detector fired.
- The bill moved and nobody can say why.
- A slow creep: a line that has roughly doubled over a quarter with no single day standing out. This is the harder and more common case, and level-based detectors never catch it.
- After a launch, migration, or load test, to confirm the cost matched the prediction.

## Procedure

### 1. Rule out billing artefacts

Before any investigation: unamortised purchases, one-off charges, credits expiring, refunds, a period boundary, a provider price change, a tax or currency effect. Each is cheap to check and each fully explains a "spike" that is not one.

### 2. Split the delta three ways

For the affected grouping, decompose the change:

- **Rate** — same usage, different price. A commitment expired or was exhausted, a discount changed, a tier boundary was crossed, the provider changed a price. Hand to `commitment-coverage`.
- **Usage** — more of the same thing at the same price. This is where deploys, flags, and traffic live.
- **Mix** — the same total usage on a differently-priced resource. An instance family changed, a storage tier changed, traffic moved to a more expensive region or path. Usually accidental and usually invisible in a service-level total.

The split is what makes triage tractable: each of the three has a different suspect list and a different owner. Do it before generating suspects.

### 3. Localise

Narrow to the smallest grouping that still contains the delta: account → service → **usage type** → region → tag. The usage type is where the mechanism lives; a service-level view will not tell you whether it was requests, storage, or transfer.

Then narrow in time: find the first day (or hour) the new level appears. That timestamp is the primary correlation key.

### 4. Generate suspects and rank them

Against the timestamp, correlate:

| Suspect class | Source | Confirm/refute test |
|---|---|---|
| deploy | deploy history | did the level change within the deploy window? does a revert restore it? |
| feature flag | flag change log | does the cost track the rollout percentage? |
| traffic change | request metrics | did the usage metric move proportionally, or did cost move alone? |
| scheduled job / backfill | orchestrator run history | does the spend align with run days rather than being continuous? |
| retention or lifecycle change | infrastructure history | is the growth monotonic rather than stepped? |
| commitment expiry | commitment inventory | does the expiry date match the step exactly? |
| provider price change | provider notices | did the unit price change while usage was flat? |
| incident | incident log | did retries or failover produce the usage? |
| new environment | resource creation history | did resources appear at the timestamp? |

Rank by correlation strength, not by plausibility. A suspect whose timestamp matches to the hour outranks a more intuitive story that is a week off.

### 5. Confirm

Run the cheapest confirming test for the top suspect. Correlation is a hypothesis; a test makes it a finding. Where the confirming test is not runnable, say so and report the finding as `CORRELATED, UNCONFIRMED` rather than as a cause.

### 6. Report and close the loop

```
## spend-anomaly-triage — <scope> — <detected date>

Billing artefacts ruled out: <list>
Delta: <$> — rate <$> · usage <$> · mix <$>
Localised to: <account> / <service> / <usage type> / <region> / <tag>
Onset: <first timestamp at the new level>

### Suspect ledger (ranked by correlation strength)
| Suspect | Class | Correlation | Confirm/refute test | Result |

Cause: <named> — CONFIRMED | CORRELATED, UNCONFIRMED | UNKNOWN
Cost of the cause: <$/period ongoing>
Remediation: <action, owner>
Detector gap: <did the detector fire? lead time? what would have caught it sooner?>
```

The detector gap line is the point of the exercise. Every triage either validates the guardrail or improves it; a triage that ends without touching `/cost-guardrails` will be repeated.

## Inputs

- Daily (ideally hourly) cost data at usage-type granularity.
- Deploy history, flag change log, orchestrator run history, incident log.
- Commitment inventory with expiry dates.
- `ai/finops/unit-economics.md` — the declared expectation, if one exists.

## Outputs

- The report block above.
- A guardrail improvement for `/cost-guardrails` — a new dimension, a tightened threshold, or a rate-of-change detector.
- Where the cause is a code change, a handoff to `@cost-reviewer` with the mechanism named, so the class is caught at diff time next occurrence.

## False positives / gotchas

- **Stopping at "service X went up".** That is the localisation step, not the cause.
- **Skipping the artefact check** and investigating a support fee for a day.
- **Correlating with the deploy that happened to be nearest.** Deploys are frequent; proximity alone is weak evidence. Use the revert or the rollout-percentage test.
- **Missing a mix change**, because the service total is flat while an instance family or storage tier changed underneath it.
- **Treating a slow creep as un-triageable.** Fit the trend, find where the slope changed, and correlate against that date instead of a single spike.
- **A weekend or holiday effect** read as a real change. Compare like days.
- **Declaring a cause without a confirming test**, then repeating the triage next month when it recurs.
- **Ending without a detector improvement**, guaranteeing a repeat.

## Related

### Skills
- `commitment-coverage` — owns the rate half of the split.
- `egress-trace` — owns transfer, the hardest usage-type to attribute.
- `unit-cost-probe` — quantifies the ongoing cost of the confirmed cause.

### Agents
- `@finops-analyst` — supplies the three-way split at scale.
- `@cost-reviewer` — receives the mechanism so the class is caught at diff time.

### Commands
- `/cost-guardrails` — receives the detector improvement; every triage should produce one.
- `/cost-model` — the declared expectation this anomaly deviated from.

### Patterns
- `ai/patterns/cost-anomaly-detection.md`, `ai/patterns/unit-economics.md`

### Cross-pack boundary
- `@incident-responder` (observability pack) owns the incident process; a cost anomaly is rarely an incident, and borrowing incident ceremony for a bill is how cost work gets ignored.
