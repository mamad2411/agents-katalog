---
name: delivery-forecasting
description: Use when throughput, WIP, service expectations, and scope boundaries must be turned into confidence-based delivery forecasts for date, scope, or commitment decisions.
---

# Delivery Forecasting

## Specialization

Convert flow signals into explicit delivery forecasts.

This skill exists to answer planning questions such as what is likely by when, what scope fits a target date, and how much confidence exists in the current commitment.

## Objective

Produce a forecast artifact with confidence ranges, assumptions, risks, and trade-off options for delivery date or scope decisions.

## Trigger Conditions

- Teams need confidence-based forecasts rather than single-point promises.
- Delivery dates are being discussed from intuition instead of flow evidence.
- Scope and date trade-offs need an explicit forecast model.
- Agents need a deterministic way to turn flow metrics into planning guidance.

## Scope Boundaries

In scope:

- Forecast inputs from throughput, WIP, and service expectations.
- Scope-date trade-off analysis.
- Confidence bands and assumption logging.
- Commitment risk statements.

Out of scope:

- Board instrumentation setup.
- Portfolio prioritization.
- Release approval.
- Staffing-model redesign.

## Inputs

- Historical throughput or comparable delivery evidence.
- Current WIP and blocked-work status.
- Scope candidate or target date.
- Service-level expectation or cycle-time policy when available.
- Known constraints, dependencies, and exceptional risks.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Forecast statement with target question and confidence bands.
- Assumption ledger listing data basis, exclusions, and special conditions.
- Scope-date trade-off table.
- Commitment risk summary with primary threats.
- Recommended decision: hold date, reduce scope, increase confidence work, or avoid commitment.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Estimate one small delivery question | One forecast statement exists |
| L2 Delivery | Support active planning with confidence ranges | Forecast, assumptions, and trade-offs are complete |
| L3 Hardening | Govern commitment quality | Commitment risk and exception conditions are explicit |
| L4 Expert Standardization | Establish reusable forecasting practice | Forecast model and assumption rules are portable across projects |

## Deterministic Workflow

1. Define the forecast question: date for scope, scope for date, or commitment confidence.
2. Gather usable historical signals and reject clearly non-comparable periods.
3. Record current WIP, blockages, and exceptional dependencies that distort normal flow.
4. Build confidence bands rather than single-point promises.
5. Write the assumptions and exclusions that shape the forecast.
6. Produce scope-date trade-off options.
7. State commitment risk in plain language.
8. Recommend one decision path and the trigger that would force recalculation.

## Forecast Rules

- Do not give a single-point commitment when the evidence only supports a range.
- If the data is weak or non-comparable, downgrade confidence rather than pretending precision.
- If blocked work or dependency risk is material, state it separately from normal throughput.
- Recalculate when scope or flow conditions materially change.

## Artifact Contract

| Artifact | Minimum Fields |
|---|---|
| Forecast statement | Question, range, confidence note, date of calculation |
| Assumption ledger | Data window, exclusions, distortions, dependency note |
| Trade-off table | Option, scope effect, date effect, confidence effect |
| Commitment risk summary | Main risks, severity, owner or trigger |

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Confidence-based forecast | Objective + Deterministic Workflow |
| Explicit assumptions | Required Outputs + Artifact Contract |
| Scope-date trade-off decision support | Required Outputs + Deterministic Workflow step 6 |
| Commitment quality control | Forecast Rules + Reasoning Package |
| Portable forecasting model | Depth Modes L4 + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- Historical flow can inform future planning when comparability is explicit.
- Confidence ranges are more truthful and useful than point estimates.

Trade-offs:

- Wider ranges improve honesty but may frustrate stakeholders seeking certainty.
- Forecast discipline improves commitments but exposes weak data quality quickly.

Open blockers:

- Sparse or unstable historical data lowers confidence.
- Major dependency volatility can dominate the forecast.

Recommendation:

- Use this skill when dates matter. It closes the gap between flow measurement and commitment quality.

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).
- Default freshness threshold is 30 days.

## Pragmatic Stop Rule

Stop when the forecast question is answered with a confidence range, assumptions are explicit, and one clear decision recommendation is recorded.

## Anti-Patterns

- Turning weak data into precise dates.
- Ignoring blocked work in forecast logic.
- Presenting ranges without naming assumptions.
- Failing to trigger recalculation after material scope change.

## Done Criteria

- All required outputs exist.
- Confidence bands are explicit.
- Assumptions and distortions are recorded.
- One recommended decision path is present.
- Source catalog entries are current for this evaluation cycle.