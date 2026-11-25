---
name: security-metrics
description: "Covers designing security metrics that drive decisions: KPI vs KRI vs metric, leading vs lagging, a concrete starter set with the action each triggers, and how to kill vanity metrics. Use when the user asks what to measure in a security program, wants KPIs or KRIs, or asks whether existing metrics are useful. (Presenting them to a board: board-metrics-reporting.)"
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Security metrics (design)

This is the **design** side: what to measure and how to make a number actionable. For
how to _present_ these to a board/exec, `load_skill board-metrics-reporting` (don't
duplicate framing here). Standards anchor: ISO/IEC 27004:2016 (ISMS measurement model:
measure → analyze → evaluate; 2016 is still the live edition, a revision is under way; verify: https://www.iso.org/standard/85920.html)
and NIST CSF 2.0 GV.OV (oversight uses metrics to adjust strategy).

## The one design rule

A measure earns its place only if a defined threshold **triggers a named action**. Write
the trigger _before_ you collect data: "if X crosses Y, then Z (who does what)." No
trigger = vanity. If you can't name what changes when it moves, delete it.

## KPI vs KRI vs metric (used loosely: be precise)

| Term       | Question it answers              | Looks at           | Owner         |
| ---------- | -------------------------------- | ------------------ | ------------- |
| **Metric** | A raw measurement                | Now                | Whoever emits |
| **KPI**    | Is the program _performing_?     | Past/now (lagging) | Process owner |
| **KRI**    | Is _risk_ rising toward a limit? | Forward (leading)  | Risk owner    |

A KPI grades you; a KRI warns you. You need both. Each KRI needs a **threshold tied to
risk appetite** (green/amber/red), not an arbitrary round number.

## Leading vs lagging: balance them

- **Lagging** (outcome, after the fact): MTTD, MTTR, incidents, breach cost. Honest but late.
- **Leading** (predictive, before impact): patch-SLA adherence, control coverage, KEV
  exposure window, phishing-report rate, % assets with EDR. These are the ones you can
  _act on_ before an incident. A deck that's all lagging is an autopsy; weight toward leading.

## Starter set (each with its trigger)

| Metric                            | Type     | What it measures                                              | Triggers                                                               |
| --------------------------------- | -------- | ------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **MTTD** (mean time to detect)    | KPI/lag  | Hours from compromise to detection                            | Rising → invest in logging/EDR coverage, tune detections               |
| **MTTR** (mean time to remediate) | KPI/lag  | Detect→contain/fix, by severity                               | Above target → IR resourcing / runbook gaps                            |
| **Patch-SLA adherence**           | KRI/lead | % criticals patched within tier SLA (e.g. crit 7d, high 30d)  | Falling → patch-pipeline blocker; below floor → escalate to risk owner |
| **KEV exposure window**           | KRI/lead | Days a CISA-KEV item stays open / oldest open KEV             | > remediation deadline → emergency change; growing backlog = red       |
| **Control coverage**              | KRI/lead | % crown-jewel assets with MFA / EDR / logging / tested backup | Any gap on a critical asset = a funded ask with a date                 |
| **Phishing-fail / report rate**   | KPI/lead | % who click vs % who report a sim                             | Click trend up or report rate low → targeted training, not blanket     |
| **Vuln backlog aging**            | KRI/lead | Age of oldest open critical; backlog trend                    | Backlog growing faster than burn-down → capacity problem               |

Set **MFA/EDR/patch SLAs to your appetite**, then benchmark against current authority,
don't hard-code memory. KEV deadlines: US federal **BOD 22-01**'s flat 14/21-day KEV clock was
**revoked by BOD 26-04 (issued 10 Jun 2026)**: an SSVC-informed remediation table keyed to
KEV status, public exposure and technical impact, shortest tier **3 days + forensic triage**,
not one clock. So a single "days open" KEV KRI now under-reports: split it by exposure tier, or
you will report green while a publicly-exposed KEV sits past its 3-day window. Verify the live
directive + catalog: https://www.cisa.gov/known-exploited-vulnerabilities-catalog . Industry phishing/MTTR
benchmarks drift yearly; cite the current Verizon DBIR / vendor report, don't assert a stale %.

## Spotting vanity metrics

Smells of a vanity metric; cut or reframe:

- **Monotonic by design**: "# vulns found", "# attacks blocked", "training completed":
  only goes up, rewards activity not outcome. Reframe to a _rate within SLA_ or _% remediated_.
- **No threshold**: a number on a slide with no green/amber/red line. Add a trigger or drop it.
- **Unactionable**: if the answer to "what would we do if this doubled?" is "nothing", it's noise.
- **Gameable**: "% compliant", "tickets closed": improve the metric without improving security.
  Pair every coverage metric with an _effectiveness_ check (control exists vs control works).
- **Activity vs outcome**: "patches deployed" is activity; "MTTR on exposed criticals" is outcome.

Rule: replace each vanity metric with the **outcome it was pretending to measure**
(see the reframe column in `board-metrics-reporting`).

## Build the metric (compact spec)

For each metric, write one line: **name | type (KPI/KRI) | formula & source | target |
threshold→action | owner | cadence.** That spec is the whole design. Store it once
(`write_file /work/metrics-catalog.md`); regenerate the report from it each cycle.

## Sourcing from marq output

- `read_file /work/findings.md` / `findings.jsonl`: confirmed findings feed the vuln-backlog
  and coverage metrics with real evidence, not guesses.
- Prioritize the backlog by exploitability before counting it: `load_skill vulnerability-prioritization`.
- Feed material metric breaches (e.g. KEV past deadline) to `report_finding` so they land
  in `render_report` alongside technical findings.

## Pairs with

- Presenting/framing metrics to leadership: `load_skill board-metrics-reporting`.
- Risk appetite that sets KRI thresholds: `load_skill risk-assessment`.
- Who acts on a triggered metric (RACI/cadence): `load_skill security-governance`.
