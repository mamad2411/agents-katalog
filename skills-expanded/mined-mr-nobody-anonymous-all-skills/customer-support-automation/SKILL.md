---
name: customer-support-automation
description: "Automate support without damaging trust: triage and routing, deflection where it works, AI drafting with human review, escalation policy and quality measurement."
type: procedural
category: communication
domain: communication
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - support ticket triage automation
  - ai support agent design
  - support deflection rate
  - escalation policy support
  - csat automation
aliases:
  - support-automation
  - helpdesk
keywords:
  - support
  - triage
  - deflection
  - escalation
  - csat
  - macros
  - routing
mcp_servers:
  - slack
  - notion
  - linear
source: custom
enabled: true
---

# Customer Support Automation

## Purpose

Automate support without damaging trust: triage and routing, deflection where it works, AI drafting with human review, escalation policy and quality measurement.

## When to Use

- Ticket volume grows faster than the team.
- Simple requests consume time that complex ones need.
- An AI first-responder is being considered.

## When NOT to Use

- Volume is low and humans handle it well.
- The product is broken; fix the cause instead of deflecting.
- Regulated advice where automation creates liability.

## Capabilities

- Classify and route tickets by intent and severity.
- Deflect with accurate self-service that measurably resolves.
- Draft replies for human review with sources and confidence.
- Define escalation triggers that never trap a customer.
- Measure deflection, CSAT and reopen rate together.

## Inputs

- Historical tickets with resolution and satisfaction data.
- The knowledge base and its accuracy.
- The SLA and the cases that legally require a human.

## Workflow

1. Mine past tickets for intents, volumes and time sinks.
2. Fix the top recurring cause in the product or docs before automating its reply.
3. Route by intent and severity with a default human queue.
4. Draft responses with citations to docs; require review until accuracy is proven.
5. Escalate on sentiment, repeat contact, or any legal keyword, unconditionally.
6. Track deflection alongside CSAT and reopen rate; a deflected-but-angry ticket is a loss.

## Tools

- zendesk
- intercom
- slack
- notion

## Examples

- `A bot that closes tickets without resolving inflates deflection and destroys CSAT simultaneously.`
- `Repeat contact within 48 hours is the clearest signal that the first answer failed.`

## Safety

- Never let automation give legal, medical or safety advice unreviewed.
- Be explicit that the customer is talking to automation, and offer a human path.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `slack` | stdio | full | medium | `SLACK_BOT_TOKEN`, `SLACK_TEAM_ID` |
| `notion` | http | standard | medium | — |
| `linear` | http | standard | medium | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/communication/customer-support-automation`). First-party skill, maintained in this repository.

## Notes

- Automate the boring and escalate the emotional; the reverse is what damages trust.
- Knowledge-base quality caps the achievable automation quality.
- Pairs with: `pricing-strategy`, `user-research`.
