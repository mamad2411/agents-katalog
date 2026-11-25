---
name: pericles-predictive
version: 2026.05.0
description: >
  How to build the predictive layer — forward-looking risk forecasts that complement the
  detect→validate→act pipeline. Use this WHENEVER you build forecasting Skills, surface
  predicted events, or compose historical signal + Org Memory + (post-§9-Phase-2)
  aggregated intelligence. Encodes that predictive Skills are pre_validation Functional
  Skills, must be evaluated against actual outcomes, and never commit actions on a
  prediction alone (proposals only, Execution Nodes commit).
doctrine_refs: [§3, §4; Manifest Spec §5]
depends_on: [pericles-functional-agent, pericles-evals-scorers, pericles-org-memory, pericles-cross-customer-learning]
last_reconciled: 2026-05-28
---

# Pericles Predictive (build skill)

Today Pericles detects and validates events as they happen; the predictive layer adds
**forward-looking forecasts**: "this corridor is likely to see disruption in the next 30
days," "your tier-2 supplier concentration is heading toward a cascade risk." It's a
post-MVP capability; build it with discipline because predictions are easy to mis-act on.

## When to use this skill

Building any forecasting Skill or surface; composing historical signal + Org Memory +
aggregated cross-customer intelligence into a forecast; deciding how a forecast is
surfaced to a persona.

## A predictive Skill is a pre_validation Functional Skill

It composes Topical/Regional/Industry knowledge and historical signal to produce a
forecast over a horizon — that's establishing truth-about-the-future, which sits on the
`pre_validation` side (`pericles-functional-agent`). It must declare `data_access.pattern
= pre_validation` and accept the registry's pipeline-position validation
(`pericles-skill-registry`).

## Sources

- **Per-tenant historical signal** — confirmed events, effective Plans, Validation
  decisions; lives in Organizational Memory (`pericles-org-memory`).
- **ERP context** — `OrganizationContext` (footprint, supplier graph, lanes) for the
  tenant whose forecast is being produced.
- **Aggregated cross-customer intelligence** — only after `pericles-cross-customer-
  learning` Phase 2 is built and audited; consume **post-aggregation outputs**, never
  per-tenant signal stores.
- **External feeds** — same untrusted-content discipline as elsewhere
  (`pericles-external-feeds`, `pericles-prompts`).

## Evals are non-negotiable

A forecast that isn't evaluated is a guess. The Skill's `eval_criteria` MUST include
**outcome-grounded scorers**: compare predicted events / windows against what actually
happened over the same horizon (calibration, Brier-style or equivalent), not just LLM-
judge plausibility. Standard promotion gate applies — every scorer above threshold, no
>5% regression (`pericles-evals-scorers`). Drift detection runs continuously.

## Surface & action boundary

Predictions are **information**, not authorization. A predictive Skill **proposes**
(e.g. "draft a Tier-1 Supplier Disruption Plan for X"); a deterministic Execution Node
commits, gated by approval (`pericles-execution-node`). Persona framing applies — a
Risk Manager sees confidence intervals and methodology; a Stakeholder sees a calibrated
narrative — `pericles-persona-layer`.

## What this forbids

A predictive Skill without outcome-grounded `eval_criteria` (mere plausibility scoring
isn't enough); committing consequential actions on a forecast without the Execution Node
+ approval; consuming per-tenant signal stores directly instead of post-aggregation
outputs (privacy); surfacing forecasts without confidence intervals to personas whose
scope includes uncertainty; masking model uncertainty in the UI.

## Verification

Pipeline position is `pre_validation` and the registry accepts it; eval suite compares
predictions to outcomes over time and gates promotion; predictions surface with
confidence intervals (where persona scope allows); proposed actions route through
Execution Nodes; cross-customer consumption is post-aggregation only.

## Existing standards (read alongside)

Doctrine §3/§4; Manifest Spec §5; `pericles-cross-customer-learning`,
`pericles-org-memory`, `pericles-functional-agent`, `pericles-evals-scorers`.

## Open questions

- Modeling approach (LLM-orchestrated stats vs trained forecasting model behind MCP).
- Horizon defaults and how the customer configures them.
- Pack-level predictive defaults — likely sit in Industry Skills
  (`pericles-industry-skill`).

## Changelog

- 2026.05.0 — Initial draft; pre_validation Functional Skill with outcome-grounded evals
  and Execution-Node-only commits.
