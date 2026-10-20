---
name: agent-platform-governance
description: Evaluate or adopt an AI-agent-building platform (Claude, Copilot Studio, or similar) using governance criteria, not just how fast a demo comes together — monitoring, integration, team sharing, identity, audit trails, and compliance, applied across the full build/govern/monitor/share/maintain lifecycle. Use when choosing between agent platforms, deciding whether an agent someone built solo is ready to hand to a team, or setting up governance before scaling agent use beyond one person.
---

# Agent Platform Governance

Source: prompted by reviewing a social-media "5 Key Learnings from Claude & Copilot Studio Testing" infographic. Its core framework (governance dimensions, lifecycle thinking) was real and worth keeping; its intro paragraph was garbled nonsense text and one specific claim (a Copilot Studio "code mode" toggle) couldn't be independently verified against current Microsoft documentation, so that detail is left out rather than repeated as fact — Copilot Studio's governance/audit/monitoring capabilities themselves *are* real and documented (agent registry, Purview audit trails, Application Insights telemetry, Sentinel alerting).

## The core mistake this framework corrects

A fast, working demo is evidence a platform is easy to *build* on. It is not evidence the resulting agent is ready to hand to a team, run unattended, or survive an audit. Comparing platforms on build speed and demo polish alone systematically favors whichever tool has the friendliest builder UI — which is a real, legitimate factor, but a different question from whether the agent is safe to operate at scale.

## Governance dimensions to actually check

When evaluating a platform (or an agent someone already built and wants to scale), check these explicitly rather than assuming they're covered because the build itself worked:

- **Monitoring** — can you see what the agent is actually doing in production, not just whether it's "running"? Logs/telemetry of individual actions, not just uptime.
- **Integration** — does it connect to the systems this agent actually needs (see this repo's own `mcp-integration-scout` agent for the Claude-side version of this check), and how much custom glue code does that integration require?
- **Team sharing** — can more than the original builder use, edit, and own this agent, or does it live in one person's personal setup?
- **Identity** — does the agent act under a traceable identity (a named account/token), or does it borrow the builder's personal credentials? The latter is a common shortcut that becomes a real liability once the agent takes side-effecting actions.
- **Audit trails** — is there a record of what the agent did and when, sufficient to reconstruct an incident after the fact? "We can check the logs" is only true if the logs are actually retained and queryable, not just technically emitted somewhere.
- **Compliance & oversight** — does the platform's governance model map onto whatever regulatory/internal-policy requirements apply to this use case, or does that get bolted on later as a separate project?

A platform can be excellent on builder experience and weak on several of these — that's a legitimate, informed trade-off to make consciously, not a gap to discover after the agent is already load-bearing.

## Full lifecycle, not just the demo

The demo output is one small part of the actual decision. Evaluate — or plan for — the whole lifecycle:

1. **Build** — the part a fast demo actually tests.
2. **Govern** — the dimensions above, set up before real usage, not retrofitted after an incident.
3. **Monitor** — ongoing visibility once it's live, not a one-time check at launch.
4. **Share** — handoff to a team: does it still work when someone other than the original builder needs to operate or modify it?
5. **Maintain** — who owns fixing it when an underlying API changes, a credential expires, or behavior drifts? An agent with no maintenance owner is a liability with a delay timer on it.

Choosing "the platform that helps you build" and "the platform that helps you run with confidence" are different evaluations — a platform can win the first and lose the second, and the second is what determines whether the agent survives contact with a real team.

## Related skills in this repo

- **web-task-scoping** / `/scope-web-task`: the same match-oversight-to-stakes discipline, applied specifically to a browser-automation task's blast radius rather than a whole platform choice.
- **night-shift-workflow** / the `night-shift-canvas` procedure: the six design decisions (Output, Trigger, Sources, Rules, Actions, Approval) for a *specific* scheduled/unattended workflow — use this skill to choose the platform first, that one to govern what runs on it.
- **mcp-integration-scout** (agent): the concrete "what's actually connected" check that the Integration dimension above describes in the abstract.
- **the-leverage-stack-auditor**: useful when a governance gap traces back to a platform choice made for speed/convenience that's now creating hidden ongoing cost.
