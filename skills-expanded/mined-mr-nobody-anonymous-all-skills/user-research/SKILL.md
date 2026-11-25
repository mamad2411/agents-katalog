---
name: user-research
description: "Run user research that changes decisions: question framing, the right method, recruiting, interview craft, synthesis and reporting so findings get acted on."
type: procedural
category: product
domain: product
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - run user interviews
  - usability testing plan
  - research synthesis findings
  - survey design bias
  - recruit research participants
aliases:
  - uxr
  - research-ops
keywords:
  - user-research
  - interviews
  - usability
  - survey
  - synthesis
  - personas
mcp_servers:
  - notion
  - filesystem
source: custom
enabled: true
---

# User Research

## Purpose

Run user research that changes decisions: question framing, the right method, recruiting, interview craft, synthesis and reporting so findings get acted on.

## When to Use

- A product decision rests on assumptions about user behaviour.
- Usability of a flow is unknown before build.
- Previous research produced reports nobody used.

## When NOT to Use

- The answer already exists in analytics data.
- The decision is irreversible and research cannot arrive in time.
- The question is a preference poll among stakeholders.

## Capabilities

- Turn a vague concern into an answerable research question.
- Pick qualitative or quantitative methods that fit the question.
- Write interview guides that avoid leading questions.
- Synthesise into findings with evidence and severity.
- Deliver decisions, not a document.

## Inputs

- The decision to be made and who makes it.
- The target participants and how to reach them.
- The timeline available before the decision.

## Workflow

1. Write the decision and the research question it needs.
2. Choose the method: interviews for why, usability for can-they, surveys for how-many.
3. Recruit participants matching the real usage conditions, including edge users.
4. Ask about past behaviour, not hypothetical intentions.
5. Synthesise in a session with the team, mapping evidence to findings.
6. Present top findings with severity, evidence quotes and a recommendation.

## Tools

- notion
- lookback
- dovetail
- maze

## Examples

- `'Would you use this?' predicts politeness; 'when did you last do this?' predicts behaviour.`
- `Five participants per segment surface most usability problems; twenty per segment mostly repeat them.`

## Safety

- Get informed consent and be explicit about recording.
- Never put identifiable participant data in shared artifacts without permission.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `notion` | http | standard | medium | — |
| `filesystem` | stdio | core | low | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/product/user-research`). First-party skill, maintained in this repository.

## Notes

- Research that arrives after the decision is documentation, not research.
- One strong quote plus a count beats ten quotes without evidence of frequency.
- Pairs with: `product-analytics`, `conversion-rate-optimization`.
