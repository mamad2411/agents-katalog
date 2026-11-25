---
name: pricing-strategy
description: "Design pricing: value metrics, packaging and tiers, willingness-to-pay research, price-change mechanics and margin safety."
type: procedural
category: product
domain: product
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - pricing strategy saas
  - value based pricing
  - packaging tiers design
  - willingness to pay research
  - price increase communication
aliases:
  - pricing
  - packaging
keywords:
  - pricing
  - packaging
  - tiers
  - willingness-to-pay
  - margin
  - discounting
mcp_servers:
  - postgres
  - stripe
  - notion
source: custom
enabled: true
---

# Pricing Strategy

## Purpose

Design pricing: value metrics, packaging and tiers, willingness-to-pay research, price-change mechanics and margin safety.

## When to Use

- A product is priced by cost-plus habit rather than value.
- Tiers confuse buyers or cannibalise the top plan.
- A price change needs a defensible migration plan.

## When NOT to Use

- The product is pre-revenue with no usage data.
- A regulated price is set externally.
- The decision is a one-off discount for a strategic account.

## Capabilities

- Choose a value metric that scales with customer benefit.
- Design packaging that separates segment needs cleanly.
- Research willingness to pay with van Westendorp and conjoint-style trade-offs.
- Model margin and revenue impact of a change.
- Plan grandfathering, notice and communication.

## Inputs

- Usage distribution and the features that actually drive retention.
- Unit economics: marginal cost per unit of usage.
- Competitor pricing and the buyer's alternative.

## Workflow

1. Identify candidate value metrics and test them against usage data.
2. Segment customers by need, not by size alone.
3. Design tiers with a clear 'why upgrade' line and no dead zone.
4. Estimate willingness to pay with structured interviews, not guesswork.
5. Model revenue and margin under the change, including churn scenarios.
6. Migrate existing customers with notice, grandfathering and a stated rationale.

## Tools

- stripe
- excel
- postgres
- amplitude

## Examples

- `Charging per seat where value scales with usage caps revenue and punishes adoption.`
- `A middle tier no one chooses is either mispriced or mispackaged.`

## Safety

- Price changes must be legally reviewable and clearly communicated.
- Avoid dark-pattern trials and hidden fees; they convert once and churn forever.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `postgres` | stdio | standard | medium | `POSTGRES_URL` |
| `stripe` | stdio | full | high | `STRIPE_SECRET_KEY` |
| `notion` | http | standard | medium | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/product/pricing-strategy`). First-party skill, maintained in this repository.

## Notes

- Discounting is a pricing decision; unbounded discount authority destroys the model.
- Test with real buyers, not with colleagues.
- Pairs with: `product-analytics`, `customer-support-automation`.
