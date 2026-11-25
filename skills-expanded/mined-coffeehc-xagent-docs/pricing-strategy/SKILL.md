---
name: pricing-strategy
description: Use when analyzing, drafting, comparing, or reviewing pricing strategy, packaging, plan design, monetization, discounting, value metric, willingness-to-pay assumptions, SaaS tiers, usage-based pricing, or pricing experiment ideas. Prefer this Skill when the task needs customer segment, value metric, offer structure, tradeoff, risk, or measurement logic. Do not use for price fixing, legal advice, or unsupported revenue guarantees.
meta:
  version: 1
  display_name: 定价策略
---

# Pricing Strategy

## Purpose

Structure pricing decisions around customer value, segments, packaging, cost-to-serve, competitive context, adoption risk, and measurable learning.

## Use When

Use for:

- SaaS pricing and packaging
- plan tier design
- usage-based pricing ideas
- discount policy drafts
- value metric analysis
- pricing experiment planning
- monetization strategy review

## Material Gate

Identify:

- customer segments, use cases, value delivered, and alternatives
- current price, cost, margin, usage, conversion, churn, and expansion data when available
- competitive references, constraints, and legal/commercial risk
- decision owner and change scope

If data is missing, frame options and assumptions rather than claiming optimal price.

## Workflow

1. Define customer segments and value drivers.
2. Identify candidate value metrics and packaging units.
3. Compare pricing models: seat, usage, tier, bundle, outcome, service, or hybrid.
4. Map tradeoffs for adoption, expansion, support cost, margin, and sales complexity.
5. Propose experiments or research needed to reduce uncertainty.
6. Separate pricing recommendation from assumptions.
7. Use `html-report-builder` for pricing comparison or monetization reports.

## Checks

- Value metric is understandable and hard to game.
- Segments are not forced into one plan without rationale.
- Discounting does not destroy price integrity.
- Legal or competitive sensitivity is flagged.
- Revenue impact is scenario-based, not guaranteed.

## Outputs

- pricing strategy brief
- packaging comparison
- plan tier proposal
- discount policy draft
- pricing experiment plan
- monetization risk summary

## Boundary

This Skill owns pricing reasoning, packaging structure, tradeoff analysis, and experiment framing. It does not own legal approval, finance approval, tax advice, price execution, billing configuration, or revenue guarantees.

It must not run shell, Python, Node, npm, curl, MCP, billing, payment, CRM, analytics, spreadsheet, package install, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
