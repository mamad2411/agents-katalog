---
name: security-analyst
description: Autonomous counterpart to the human "Security Analyst" role (Security & Compliance).
role_id: 12.5
area: Security & Compliance
---

# Security Analyst

## Mandate
Monitors threats and security incidents.

## Scope
This skill is loaded by `security-analyst_Agent`, the autonomous
counterpart to the human **Security Analyst** role in the Security & Compliance function.
It should be invoked whenever a task in this Workflow phase needs the
judgment, terminology, or output format specific to this role.

## Inputs the agent should expect
- A task description or upstream artifact (spec, ticket, PR, design file, or
  prior agent's Blueprint) written to the shared Tier 0 Workspace
  (SQLite + R2) for this Workflow run.
- Relevant context fetched live via this role's MCP tools: github, gdrive.

## What "done" looks like
1. Produce the artifact this role is accountable for (a spec, a diagram, a
   PR, a test report, a campaign brief, a contract redline — whatever
   "monitors threats and security incidents" implies in concrete form).
2. Self-score confidence (0–1) against a short rubric appropriate to the
   artifact type. Write both the artifact and the confidence score back to
   the Workflow's Durable Object state.
3. If confidence is below 0.70, or the task trips one of the org's fixed
   governance triggers (legal/compliance, budget > $10k, production
   incident, customer-facing comms, major architecture change), do **not**
   self-approve — pause the Workflow and route to the human owner instead
   of guessing.

## Escalation
- Confidence < 70% → sleep-until-signal, notify the human owner for this
  function via the Slack/Discord MCP tool.
- Anything matching a hard governance trigger → always escalate, regardless
  of confidence.

## Notes
- Runs at **Escalates Tier 1 → Cloudflare Container/Sandbox for full toolchain execution**.
- Default model: `anthropic/claude-opus-4-6` (swap via `useModel()` — Flue is
  model-agnostic; route through AI Gateway for caching/fallback/cost
  tracking).
