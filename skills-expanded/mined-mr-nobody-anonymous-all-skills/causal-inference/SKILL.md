---
name: causal-inference
description: "Estimate causal effects from observational data: DAGs and confounding, matching and weighting, difference-in-differences, instrumental variables and honest sensitivity analysis."
type: procedural
category: scientific
domain: scientific
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - causal inference observational data
  - difference in differences
  - propensity score matching
  - confounding variable dag
  - instrumental variable analysis
aliases:
  - causal
keywords:
  - causal-inference
  - confounding
  - dag
  - did
  - matching
  - instrument
  - sensitivity
mcp_servers:
  - filesystem
  - duckdb
source: custom
enabled: true
---

# Causal Inference

## Purpose

Estimate causal effects from observational data: DAGs and confounding, matching and weighting, difference-in-differences, instrumental variables and honest sensitivity analysis.

## When to Use

- A decision needs an effect size and a randomised experiment is impossible.
- Correlation is being reported as if it were causal.
- A policy or product change must be evaluated after the fact.

## When NOT to Use

- A randomised experiment is feasible and affordable.
- The question is descriptive rather than causal.
- There is no plausible identification strategy.

## Capabilities

- Draw the causal graph and name the confounders and colliders.
- Choose an identification strategy that the data can support.
- Balance covariates with matching or weighting and check overlap.
- Estimate effects with robust uncertainty and clustering.
- Quantify how strong an unobserved confounder would have to be to overturn the result.

## Inputs

- The treatment, outcome and the mechanism linking them.
- Panel or cross-sectional data with pre/post or instrument availability.
- Domain knowledge to justify assumptions, written down.

## Workflow

1. Write the DAG before touching the data, and list the assumptions it encodes.
2. Check positivity and overlap before estimating anything.
3. Pick the design: matching, DiD, IV, or regression discontinuity.
4. Pre-specify the model and the covariates; do not fish for significance.
5. Run placebo and pre-trend checks where the design allows.
6. Report a sensitivity analysis and state what would falsify the conclusion.

## Tools

- python
- r
- statsmodels
- dowhy
- econml

## Examples

- `Parallel trends is an assumption, not a finding — plot pre-period trends before a DiD claim.`
- `A result that flips with one plausible unobserved confounder is not a decision input.`

## Safety

- Never present an observational estimate as an experimental one.
- Document assumptions where readers can challenge them; hidden assumptions are the failure mode.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `filesystem` | stdio | core | low | — |
| `duckdb` | stdio | standard | medium | `MOTHERDUCK_TOKEN`, `DUCKDB_PATH` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/scientific/causal-inference`). First-party skill, maintained in this repository.

## Notes

- The DAG is the analysis; the regression is bookkeeping.
- Cluster standard errors at the level of treatment assignment.
- Pairs with: `statistics`, `model-drift-monitoring`.
