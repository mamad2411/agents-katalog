---
name: probabilistic-forecasting
description: Use when throughput data, cycle time records, or flow signals must be turned into confidence-based forecasts using simulation or percentile mechanics — covering Monte Carlo simulation, cycle time scatterplots, throughput histograms, and percentile-based service level agreements.
---

# Probabilistic Forecasting

## Specialization

Convert flow data into explicit probabilistic forecasts using quantitative mechanics.

This skill is the method-level complement to `delivery-forecasting`. Where `delivery-forecasting` owns the forecast artifact contract, risk framing, and decision recommendation, this skill teaches *how* to build confidence bands from data: which calculation to use, how to read the result, and what the numbers mean for commitment decisions.

## Objective

Produce a forecast grounded in simulation or percentile mechanics with explicit data inputs, calculation method, confidence bands, and interpretation guidance — replacing intuition and point estimates with evidence.

## Trigger Conditions

- A team needs a date or scope forecast but only has throughput counts, cycle time records, or flow metrics rather than intuition.
- `delivery-forecasting` produced a confidence range but no calculation method was specified.
- A commitment is being made for a fixed-scope or fixed-date delivery that has material consequences if missed.
- Stakeholders are demanding a single-point date and the team needs a principled way to respond with confidence ranges instead.
- Existing estimates are consistently late or consistently early, signaling a calibration problem.

## Scope Boundaries

In scope:

- Throughput-based Monte Carlo simulation for scope delivery forecasting.
- Cycle time percentile analysis for single-item service level expectations.
- Throughput histogram construction and shape interpretation.
- Cycle time scatterplot construction and aging analysis.
- Percentile-based SLA design (50th, 85th, 95th).
- Assumption and comparability review of historical data.
- Confidence band interpretation and commitment guidance.

Out of scope:

- Flow policy design and WIP limit setting (use `flow-metrics`).
- Forecast decision artifacts and commitment risk summaries (use `delivery-forecasting`).
- Story point estimation and velocity-based planning.
- Team capacity modelling.
- Tool-specific configuration for forecasting software.

## Inputs

- Historical throughput: items completed per time unit (week is preferred) for a comparable period.
- Historical cycle time: elapsed time from started to finished per item, with item type noted.
- Target scope: number of items to be delivered, or item types if mixed.
- Target date (optional): needed for scope-for-date questions.
- Data comparability notes: periods to exclude (holidays, team changes, dependency freezes).
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Data review: comparable period selected, exclusions listed, data shape described.
- Simulation or percentile result: confidence bands at 50th, 85th, and 95th percentile.
- Histogram or scatterplot interpretation: distribution shape, outlier note, tail risk.
- Service level expectation (SLE): stated as "X% of items of this type are completed within N days."
- Interpretation note: what the result means in plain language for a commitment decision.
- Data quality flag: whether the data is strong enough to produce a reliable forecast.

## Calculation Methods

### Throughput-Based Monte Carlo Simulation (scope delivery)

Use when: you have a scope in items and want to know the likely delivery date range.

How it works:
1. Gather weekly throughput for a comparable period (minimum 8 weeks recommended; 12 or more is preferred).
2. Remove clearly non-comparable weeks (holiday weeks, forced pauses, major team events).
3. Record the throughput distribution as a list of weekly counts.
4. Run the simulation: for each trial, randomly sample throughput values from the historical distribution and accumulate until the target scope is reached. Record the week count.
5. Run at least 10,000 trials.
6. Read the percentile results: the 50th percentile is the median completion date; the 85th is the high-confidence date; the 95th is the near-certainty date.
7. Report all three. Recommend the 85th percentile for commitments with material consequences.

Rules:
- Do not average throughput into a single number before simulation. Averaging erases the distribution and loses risk information.
- If the distribution has a heavy right tail (outlier low-throughput weeks), note it explicitly and explain the tail risk to the commitment decision.
- If fewer than 8 comparable weeks are available, downgrade confidence and state the data limitation.

### Cycle Time Percentile Analysis (single-item SLE)

Use when: you want to set a service level expectation for how long a single item should take.

How it works:
1. Gather cycle time records for items of the same type from a comparable period.
2. Plot or sort by cycle time from shortest to longest.
3. Calculate the 50th, 85th, and 95th percentile.
4. State the SLE as: "X% of [item type] items are completed within N days."
5. Use the 85th percentile as the default SLE for teams starting out; adjust based on tolerance for exceptions.

Rules:
- Do not mix item types without acknowledging that the distribution will be biased toward the larger type.
- If cycle time has been trending upward over the period, the percentile will lag behind current reality. Trim the dataset to a more recent window and note it.
- Aging items on the board that are not yet finished should be tracked separately as leading indicators of future right-tail risk.

### Throughput Histogram Shape Interpretation

| Shape | What It Signals | Action |
|---|---|---|
| Approximately normal, narrow spread | Stable, predictable flow | Low-adjustment forecast |
| Wide spread, symmetric | High variability; WIP or interruption problem | Widen confidence bands; flag for flow review |
| Right-skewed (few high-throughput weeks) | Occasional bursts; inconsistent flow | Note burst dependency; do not rely on peak weeks |
| Left-skewed (few low-throughput weeks) | Occasional disruptions; generally strong flow | The 85th percentile will absorb disruptions adequately |
| Bimodal | Two distinct operating modes (e.g. sprint vs. holiday cadence) | Separate the populations before forecasting |

### Cycle Time Scatterplot Aging Analysis

- Plot items by completion date (x-axis) and cycle time in days (y-axis).
- Draw the 50th, 85th, and 95th percentile lines horizontally.
- Items above the 95th line are tail-risk cases; investigate systemic causes.
- Items currently on the board that are aging past the 85th percentile are at risk of becoming outliers; flag for escalation.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Produce one percentile-based estimate | A confidence band with 50th/85th/95th percentiles exists |
| L2 Delivery | Produce a Monte Carlo forecast for active planning | Simulation run, data review, and interpretation note are complete |
| L3 Hardening | Calibrate forecasting practice against delivery history | SLE is defined, data quality is reviewed, and tail-risk is explicitly named |
| L4 Expert Standardization | Establish a portable, reusable probabilistic forecasting model | Methods, data rules, and SLE definitions are documented and usable across projects |

## Deterministic Workflow

1. Classify the question: scope-for-date, date-for-scope, or single-item SLE.
2. Gather the data and review comparability. Remove non-comparable periods and document exclusions.
3. Describe the data shape: mean, range, outlier weeks, and trend direction.
4. Select the calculation method: Monte Carlo for multi-item scope questions; percentile for single-item SLE.
5. Run the calculation. For Monte Carlo: minimum 10,000 trials, report 50th/85th/95th.
6. Interpret the result in plain language: what the 85th percentile means for this commitment.
7. Flag data quality: is the dataset large enough and comparable enough for reliable output?
8. Recommend a commitment posture: accept the 85th percentile, request scope reduction, or decline commitment pending better data.

## Forecast Rules

- Always report three percentiles (50th, 85th, 95th). Never report only the 50th as if it were the commitment.
- The 85th percentile is the default commitment reference for delivery work with material consequences.
- If data quality is low (fewer than 8 weeks, high non-comparability), lower the confidence tier and state it explicitly.
- Never average throughput into a velocity before running simulation. The distribution is the signal.
- Do not generate a forecast for scope that has not been itemized to a comparable granularity level.

## Artifact Contract

| Artifact | Minimum Fields |
|---|---|
| Data review | Period, item count, exclusions, shape description, quality flag |
| Simulation result | Method used, trial count, 50th percentile, 85th percentile, 95th percentile, target question |
| SLE statement | Item type, percentile level, day count, data period |
| Interpretation note | Plain-language meaning, commitment reference percentile, tail-risk note |
| Data quality flag | Sufficient / Marginal / Insufficient with one-line reason |

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Forecast method selection | Calculation Methods section |
| Monte Carlo mechanics | Throughput-Based Monte Carlo Simulation |
| Cycle time SLE design | Cycle Time Percentile Analysis |
| Distribution shape reading | Throughput Histogram Shape Interpretation |
| Aging item risk detection | Cycle Time Scatterplot Aging Analysis |
| Commitment posture guidance | Forecast Rules + Deterministic Workflow step 8 |

## Reasoning Package

Assumptions:

- Historical flow data is a useful proxy for future performance when comparability is verified.
- Percentile-based commitments are more honest and more useful than point estimates.

Trade-offs:

- Probabilistic outputs require stakeholders to accept ranges rather than dates, which can create communication friction.
- Monte Carlo results are only as good as the comparability of the input data; bad data produces confidently wrong forecasts.

Open blockers:

- Teams with fewer than 8 weeks of throughput history need supplemental context or must accept marginal confidence.
- Mixed item types in the same dataset distort distributions; separating them is worth the overhead.

Recommendation:

- Use this skill alongside `delivery-forecasting` whenever a commitment has material consequences. Use `delivery-forecasting` for the artifact contract and decision record; use this skill for the calculation mechanics that justify the confidence bands.

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).
- Default freshness threshold is 30 days.

## Pragmatic Stop Rule

Stop when the forecast question is answered with a stated percentile method, three confidence bands are present, data quality is flagged, and the interpretation is in plain language.

## Anti-Patterns

- Reporting only the median as the commitment date.
- Averaging throughput before simulation (destroys distribution information).
- Using data from non-comparable periods without noting the distortion.
- Mixing item types without acknowledging the bias.
- Ignoring aging items when they are leading indicators of tail risk.
- Producing a forecast without a data quality flag.

## Done Criteria

- Forecast question is classified.
- Data review is complete with exclusions noted and quality flagged.
- Calculation method is selected and applied correctly.
- Three confidence bands (50th, 85th, 95th) are reported.
- Interpretation note is in plain language.
- Commitment recommendation is present.
- Source catalog entries are current for this evaluation cycle.
