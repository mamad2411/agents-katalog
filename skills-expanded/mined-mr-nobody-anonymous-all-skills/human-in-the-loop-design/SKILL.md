---
name: human-in-the-loop-design
description: "Design human approval into agent workflows: risk-tiered gates, reviewable diffs, timeout and escalation policy, audit trail and reversible actions."
type: procedural
category: agents
domain: agents
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - agent approval gate
  - human in the loop design
  - agent escalation policy
  - approve before destructive action
  - agent audit trail
aliases:
  - hitl
keywords:
  - human-in-the-loop
  - approval
  - escalation
  - audit
  - reversible
  - policy
mcp_servers:
  - filesystem
  - github
  - slack
source: custom
enabled: true
---

# Human-in-the-Loop Design

## Purpose

Design human approval into agent workflows: risk-tiered gates, reviewable diffs, timeout and escalation policy, audit trail and reversible actions.

## When to Use

- An agent can take actions with real-world consequences.
- Regulation or policy requires a named human to approve.
- A previous incident came from an unreviewable automated decision.

## When NOT to Use

- The action is read-only and reversible with no cost.
- Approval would be pure theatre because nobody reads it.
- Latency requirements make synchronous approval impossible — design async then.

## Capabilities

- Classify actions by blast radius and reversibility.
- Present diffs and previews, not prose descriptions, for approval.
- Define what happens when nobody answers: pause, expire or escalate.
- Keep an immutable audit record of who approved what, when.
- Design rollback for every approved action.

## Inputs

- The action catalogue with risk, reversibility and cost.
- The people who can approve each class, and their response-time reality.
- The compliance requirement that applies.

## Workflow

1. Tier actions: read, draft, reversible write, irreversible write, spend.
2. Require approval only for the tiers that need it, with a clear preview payload.
3. Route approvals to the right person with a deadline and a default action.
4. Record approvals with actor, action hash, timestamp and the artifact shown.
5. Make each approved action reversible or compensable and document how.
6. Review the audit log periodically for rubber-stamping.

## Tools

- slack
- github
- filesystem

## Examples

- `Showing the exact file diff for approval beats 'the agent will update the config' — reviewers approve what they can see.`
- `An approval that expires into 'reject' prevents a stalled task from auto-executing later.`

## Safety

- Never let the agent approve its own action or widen its own permissions.
- Approval fatigue is a security bug: too many low-value gates train people to click yes.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `filesystem` | stdio | core | low | — |
| `github` | http | standard | medium | `GITHUB_PERSONAL_ACCESS_TOKEN` |
| `slack` | stdio | full | medium | `SLACK_BOT_TOKEN`, `SLACK_TEAM_ID` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/agents/human-in-the-loop-design`). First-party skill, maintained in this repository.

## Notes

- Approvals should be asynchronous with a bounded wait, not blocking forever.
- Log the diff shown, not just the action taken.
- Pairs with: `agent-reliability`, `agent-observability`.
