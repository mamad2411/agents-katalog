---
name: capacitor-performance-quality-gate
description: Use when a CapacitorJS change needs an expert, evidence-first performance decision with deterministic startup, rendering, memory, bridge-latency, and regression checks before merge or promotion.
---

# Capacitor Performance Quality Gate

## Specialization

Issue an evidence-based pass/fail recommendation for CapacitorJS performance across startup, interaction latency, memory behavior, and native bridge cost.

## Trigger Conditions

- A Capacitor feature introduces measurable UI or startup lag.
- A release candidate needs a performance go/no-go decision.
- Performance regressions are suspected after plugin or framework upgrades.

## Inputs

- Target devices and OS versions.
- Performance budgets (startup, frame time, memory, bridge latency).
- Baseline build and candidate build.
- Test scenarios and expected user journeys.

## Required Outputs

- Severity-ranked findings with measured deltas vs baseline.
- Budget compliance table and gate verdict.
- Root-cause hypotheses and prioritized remediation actions.
- Residual risk statement for release decisioning.

## Deterministic Workflow

1. Lock device matrix and test scenarios.
2. Capture baseline metrics under controlled conditions.
3. Capture candidate metrics using the same protocol.
4. Compare deltas against explicit budgets.
5. Classify regressions by severity and user impact.
6. Publish one gate verdict: pass, conditional pass, or fail.

## Core Metrics

- Cold start to first interactive screen.
- Average and p95 frame time on core flows.
- Memory footprint after sustained interaction.
- Bridge call latency for plugin-heavy flows.
- Input latency for critical UI actions.

## Quality Gates

- No critical journey exceeds approved latency budget.
- Memory growth does not indicate leak risk during steady-state use.
- Regressions are statistically stable across repeat runs.
- Verdict includes traceable evidence and owner-assigned actions.

## Done Criteria

- Performance verdict is explicit and evidence-backed.
- High-severity regressions have assigned owners and fixes.
- Release recommendation includes residual risk and follow-up checks.
